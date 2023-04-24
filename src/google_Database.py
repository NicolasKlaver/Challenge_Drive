import mysql.connector
import json
import datetime
import sys


class Database:
    def __init__(self, user, password, host):
        self.user = user
        self.password = password
        self.host = host
        self.connection = None
        self.cursor = None

    """
    def __enter__(self):
        self.open_connection()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()
    """
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
        
    def create_database(self, db_name):
        try:
            self.cursor = self.connection.cursor()
            sql= "CREATE DATABASE IF NOT EXISTS {}".format(db_name)
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
    
##################### A PARTIR DE AQUI ES EL CODIGO QUE ANDABA --> REVISAR#####################
    def insert_data(self, table_name, data):
        try:
            data_unique= self.get_unique_data(data)
            
            # Cargar los datos JSON en un objeto Python
            data_json= json.dumps(data_unique)
            data_dict = json.loads(data_json)
        
            # Crear el cursor
            self.cursor = self.connection.cursor()


            # Ejecutar la consulta para cada conjunto de datos en la lista
            for item in data_dict:
                # Construir la consulta SQL
                sql = """INSERT INTO {} 
                    (name, extension, owner, visibility, fecha_ultima_modificacion, was_public)
                    VALUES (%s, %s, %s, %s, %s, %s)""".format(table_name)

            
                # Convertir el valor de was_public a un booleano
                was_public = 1 if item.get('visibility', '') == 'publico' else 0
            
                values = (
                    item['name'],
                    item['extension'],
                    item['owner'],
                    item['visibility'],
                    item['fecha_ultima_modificacion'],
                    was_public
                    )
                self.cursor.execute(sql, values)
            
            self.connection.commit()

            print(f"Se han insertado {len(data_dict)} registros exitosamente.")
        except mysql.connector.Error as err:
            print(f"Error al insertar datos: {err}")
    
    def update_visibility(self, table_name, new_visibility='privado'):
        try:
            # Crear el cursor
            self.cursor = self.connection.cursor()

            # Consulta SQL para actualizar los registros
            sql = f"UPDATE {table_name} SET visibility = %s, fecha_ultima_modificacion = %s WHERE visibility = %s"
            
            # Obtener la fecha y hora actual
            current_date_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Ejecutar la consulta para actualizar los registros
            self.cursor.execute(sql, (new_visibility, current_date_time, 'publico'))

            # Guardar los cambios en la base de datos
            self.connection.commit()

            print(f"Se han actualizado {self.cursor.rowcount} registros.")
        
        except mysql.connector.Error as err:
            print(f"Error al actualizar los registros: {err}")
            
    def update_last_modified_date(self, existing_data, new_data, table_name):
    
        # Tengo que cambiar el campo de datatime a string para poder comparar
        # for item in existing_data:
        # item['fecha_ultima_modificacion'] = item['fecha_ultima_modificacion'].strftime("%Y-%m-%d %H:%M:%S")
        try:
            # Crear el cursor
            self.cursor = self.connection.cursor()

            # Consulta SQL para actualizar los registros
            sql = f"UPDATE {table_name} SET fecha_ultima_modificacion = %s "
            
            # Obtener la fecha y hora actual

            # Ejecutar la consulta para actualizar los registros
            self.cursor.execute(sql, ())

            # Guardar los cambios en la base de datos
            self.connection.commit()

            print(f"Se han actualizado {self.cursor.rowcount} registros.")
        
        except mysql.connector.Error as err:
            print(f"Error al actualizar los registros: {err}")
           
    def select_all_data(self, table_name):
        try:
            #self.cursor = self.connection.cursor(dictionary=True)
            self.cursor = self.connection.cursor()

            sql = f"SELECT name, extension, owner, visibility, fecha_ultima_modificacion FROM {table_name}"
            self.cursor.execute(sql)
            
            return self.cursor.fetchall()
        
        except mysql.connector.Error as err:
            print(f"Error al seleccionar los datos: {err}")

##################### A PARTIR DE AQUI ES EL CODIGO NUEVO --> PROBAR #####################
    def get_files_list(self):
        try:
            #self.cursor = self.connection.cursor(dictionary=True)
            self.cursor = self.connection.cursor()

            sql = f"SELECT name, extension, owner, visibility, fecha_ultima_modificacion, was_public FROM Inventario"
            self.cursor.execute(sql)
            
            return self.cursor.fetchall()
        
        except mysql.connector.Error as err:
            print(f"Error al seleccionar los datos: {err}")

    def buscar_archivo(self, file_name, file_extension):
        self.cursor = self.connection.cursor()
        
        self.cursor.execute("SELECT * FROM tabla WHERE name={file_name} AND extension={file_extension}}")
        result= self.cursor.fetchall()
        
        if len(result) > 0:
            return True
        else:
            return False

    def insertar_archivo(self, file_name, file_extension, file_owner, file_visibility, file_last_modified_date, file_was_public):
        # Crear el cursor
        self.cursor = self.connection.cursor()
        
        sql= "INSERT INTO Inventario (name, extension, owner, visibility, fecha_ultima_modificacion, was_public) VALUES (%s, %s, %s, %s, %s, %s)"
        
        values = ( file_name, file_extension,file_owner,file_visibility,file_last_modified_date,file_was_public)
        
        self.cursor.execute(sql, values)
        self.cursor.commit()

    def insertar_archivo_historico(self, file_name, file_extension, file_owner, file_visibility, file_last_modified_date):
        # Crear el cursor
        self.cursor = self.connection.cursor()
        
        sql= "INSERT INTO Inventario_Historico (name, extension, owner, visibility, fecha_ultima_modificacion, was_public) VALUES (%s, %s, %s, %s, %s, %s)"
        
        values = ( file_name, file_extension,file_owner,file_visibility,file_last_modified_date)
        
        self.cursor.execute(sql, values)
        self.cursor.commit()
    
    def fue_modificado(self, file_name, file_extension, file_last_modified_date):
        
        sql= "SELECT fecha_ultima_modificacion FROM Inventario WHERE name={file_name} AND extension={file_extension}}"
        
        ultima_modificacion= self.cursor.execute(sql)

        if ultima_modificacion != file_last_modified_date:
            return True
        else:
            return False

    def update_last_modified_date(self, file_last_modified_date):
        self.cursor = self.connection.cursor()
        sql= "UPDATE Inventario SET fecha_ultima_modificacion={file_last_modified_date} WHERE name={file_name} AND extension={file_extension}}"
        self.cursor.execute(sql)
        self.cursor.commit()

    def cambiar_visibilidad(self, file_name, file_extension, file_modified_time):
        self.cursor = self.connection.cursor()
        sql= "UPDATE Inventario SET visibility={file_visibility} WHERE name={file_name} AND extension={file_extension}}"
        self.cursor.execute(sql)
        self.cursor.commit()




db = Database(host="localhost", user="root", password="root")
db.open_connection()
#db.create_database("mydatabaseTest")
db.select_database("mydatabaseTest") 
#db.create_table("Inventario")

data= [
  {
    "name": "documento1",
    "extension": "pdf",
    "owner": "usuario12@gmail.com",
    "visibility": "publico",
    "fecha_ultima_modificacion": "2022-04-19 13:00:00"
  },
  {
    "name": "imagen1",
    "extension": "png",
    "owner": "usuario2@gmail.com",
    "visibility": "privado",
    "fecha_ultima_modificacion": "2022-04-18 10:30:00"
  },
  {
    "name": "documento",
    "extension": "docx",
    "owner": "usuario3@gmail.com",
    "visibility": "privado",
    "fecha_ultima_modificacion": "2022-04-17 14:45:00"
  }
    ]

db.insert_data(table_name="Inventario", data = data)
#db.update_visibility(table_name="Inventario")

db.close_connection()