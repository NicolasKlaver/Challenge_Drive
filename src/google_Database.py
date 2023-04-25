import mysql.connector
#import json
#import datetime
#from google_DriveAPI import GoogleDriveAPI
#from google_DriveInventory import GoogleDriveInventory
#import google_DriveAPI
#import google_DriveInventory

class Database:
    def __init__(self, user, password, host):
        self.user = user
        self.password = password
        self.host = host
        self.connection = None
        self.cursor = None

    def open_connection(self):
        self.connection = mysql.connector.connect(
            user=self.user,
            password=self.password,
            host=self.host,
        )
        print("Conectado a MySQL con Exito")
        
    def close_connection(self):
        try:
            if self.cursor is not None:
                self.cursor.close()
            if self.connection is not None:
                self.connection.close()
        except Exception as e:
            print(f"Error al cerrar la conexión: {e}")
        
    def create_database(self,db_name):
        #create_database(self, db_name):
        try:
            self.cursor = self.connection.cursor()
            #sql= "CREATE DATABASE IF NOT EXISTS {db_name}}".format(db_name)
            sql= "CREATE DATABASE IF NOT EXISTS {db_name}".format(db_name=db_name)
            self.cursor.execute(sql)
            print("La base de datos se ha creado exitosamente.")
        except mysql.connector.Error as err:
            print(f"Error al crear la base de datos: {err}")
      
    def select_database(self, db_name):
        try:
            self.connection.database = db_name
        except mysql.connector.Error as err:
            print(f"Error al conectarse a la base de datos: {err}")
        
    def create_table(self, table_name):
        try: 
            self.cursor = self.connection.cursor()
            sql = """CREATE TABLE IF NOT EXISTS {} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                extension VARCHAR(50),
                owner VARCHAR(255),
                visibility ENUM('publico', 'privado'),
                fecha_ultima_modificacion DATETIME,
                was_public BOOLEAN
              )""".format(table_name)
              
            self.cursor.execute(sql)
            print("La tabla se ha creado exitosamente.")
        except mysql.connector.Error as err:
            print(f"Error al crear la tabla: {err}")    
    
##################### A PARTIR DE AQUI ES EL CODIGO NUEVO --> PROBAR #####################
    def get_files_list(self):
        try:
            #self.cursor = self.connection.cursor(dictionary=True)
            self.cursor = self.connection.cursor()

            sql = f"SELECT name, extension, owner, visibility, fecha_ultima_modificacion, was_public FROM InventarioIntegracion"
            self.cursor.execute(sql)
            
            return self.cursor.fetchall()
        
        except mysql.connector.Error as err:
            print(f"Error al seleccionar los datos: {err}")

    def buscar_archivo(self, file_name, file_extension):
        self.cursor = self.connection.cursor()
    
        sql = "SELECT * FROM InventarioIntegracion WHERE name=%s AND extension=%s"
        self.cursor.execute(sql, (file_name, file_extension))
        
        result= self.cursor.fetchall()
        
        if len(result) > 0:
            return True
        else:
            return False

    def insertar_archivo_nuevo(self, file_name, file_extension, file_owner, file_visibility, file_last_modified_date, file_was_public):
        # Crear el cursor
        print("imprimiendo desde la base de datos", )
        self.cursor = self.connection.cursor()
        
        sql= "INSERT INTO InventarioIntegracion (name, extension, owner, visibility, fecha_ultima_modificacion, was_public) VALUES (%s, %s, %s, %s, %s, %s)"
        
        values = ( file_name, file_extension,file_owner,file_visibility,file_last_modified_date,file_was_public)
        
        self.cursor.execute(sql, values)
        print("Se ha insertado el archivo exitosamente.")
        self.connection.commit()

    def insertar_archivo_historico(self, file_name, file_extension, file_owner, file_visibility, file_last_modified_date):
        # Crear el cursor
        self.cursor = self.connection.cursor()
        
        sql= "INSERT INTO Inventario_Historico (name, extension, owner, visibility, fecha_ultima_modificacion, was_public) VALUES (%s, %s, %s, %s, %s, %s)"
        
        values = ( file_name, file_extension,file_owner,file_visibility,file_last_modified_date)
        
        self.cursor.execute(sql, values)
        self.connection.commit()
    
    def fue_modificado(self, file_name, file_extension, file_last_modified_date):
        
        sql= "SELECT fecha_ultima_modificacion FROM InventarioIntegracion WHERE name={file_name} AND extension={file_extension}}"
        
        ultima_modificacion= self.cursor.execute(sql)

        if ultima_modificacion != file_last_modified_date:
            return True
        else:
            return False

    def update_last_modified_date(self, file_last_modified_date):
        self.cursor = self.connection.cursor()
        sql= "UPDATE InventarioIntegracion SET fecha_ultima_modificacion={file_last_modified_date} WHERE name={file_name} AND extension={file_extension}}"
        self.cursor.execute(sql)
        self.cursor.commit()

    def cambiar_visibilidad(self, file_name, file_extension, file_modified_time):
        self.cursor = self.connection.cursor()
        sql= "UPDATE InventarioIntegracion SET visibility={file_visibility} WHERE name={file_name} AND extension={file_extension}}"
        self.cursor.execute(sql)
        self.cursor.commit()


