import mysql.connector
import datetime


class Database:
    ########## FUNCION DE INICIALIZACION ##########
    def __init__(self, user, password, host):
        self.user = user
        self.password = password
        self.host = host
        self.connection = None
        self.cursor = None
        self.table_inv= None
        self.table_historico= None


    ########## FUNCION DE CONEXIONES ##########
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
        
        
    ########## FUNCION DE CRACION DE BASE DE DATOS Y TABLAS ##########
    def create_database(self, db_name):
        try:
            self.cursor = self.connection.cursor()
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
        
    def create_table_inventario(self, table_name):
        #Asigno el valor del nombre de la tabla 
        self.table_inv = table_name
        print("\nTabla inventario: ",  self.table_inv)

        try:
            self.cursor = self.connection.cursor()
            sql = """CREATE TABLE IF NOT EXISTS {} (
                id VARCHAR(100) PRIMARY KEY,
                name VARCHAR(255),
                extension VARCHAR(50),
                owner VARCHAR(255),
                visibility ENUM('publico', 'privado'),
                fecha_ultima_modificacion DATETIME,
                was_public BOOLEAN
              )""".format(self.table_inv)
              
            self.cursor.execute(sql)
            print("La tabla de Inventario se ha creado exitosamente.")
        except mysql.connector.Error as err:
            print(f"Error al crear la tabla: {err}")    
    
    def create_table_historico(self, table_name):
        self.table_historico = table_name
        print("\n\nTabla Historico: ",  self.table_historico)
        try: 
            self.cursor = self.connection.cursor()
            sql = """CREATE TABLE IF NOT EXISTS {} (
                id VARCHAR(100) PRIMARY KEY,
                name VARCHAR(255),
                extension VARCHAR(50),
                owner VARCHAR(255),
                fecha_ultima_modificacion DATETIME
              )""".format(self.table_historico)
              
            self.cursor.execute(sql)
            print("La tabla Historica se ha creado exitosamente.")
        except mysql.connector.Error as err:
            print(f"Error al crear la tabla: {err}")   
    
    
    ########## FUNCION PARA INSERTAR ARCHIVOS EN LA BASE DE DATOS ##########
    def insertar_archivo_nuevo(self, file, file_was_public):
        file_id = file['id']
        file_name = file['name']
        file_extension= file['extension']
        #file_owner = file['owners'][0]['emailAddress']
        file_owner = file['owner']
        file_visibility = file['visibility']
        file_modified_time = datetime.datetime.strptime(file['modified_time'], '%Y-%m-%dT%H:%M:%S.%fZ')

        # Crear el cursor
        self.cursor = self.connection.cursor()
        sql= f"INSERT INTO {self.table_inv} (id, name, extension, owner, visibility, fecha_ultima_modificacion, was_public) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        
        values = (file_id, file_name, file_extension,file_owner,file_visibility,file_modified_time, file_was_public)
        
        self.cursor.execute(sql, values)
        print("Se ha insertado el archivo exitosamente.")
        self.connection.commit()

    def insertar_archivo_historico(self, file):
        file_id = file['id']
        file_name = file['name']
        file_extension= file['extension']
        #file_owner = file['owners'][0]['emailAddress']
        file_owner = file['owner']
        file_modified_time = datetime.datetime.strptime(file['modified_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
        
        # Crear el cursor
        self.cursor = self.connection.cursor()
        sql= f"INSERT INTO {self.table_historico} (id, name, extension, owner, fecha_ultima_modificacion) VALUES (%s, %s, %s, %s, %s)"
        
        values = ( file_id, file_name, file_extension,file_owner,file_modified_time)
        
        self.cursor.execute(sql, values)
        self.connection.commit()
    
    
    ########## FUNCION QUE DEVUELVE LOS ARCHIVOS ???????? ##########
    def pedido_archivos_inventario(self):
        try:
            self.cursor = self.connection.cursor()

            sql = f"SELECT * FROM {self.table_inv}"
            self.cursor.execute(sql)

            rows= self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            
            return [dict(zip(columns, row)) for row in rows]
        
        except mysql.connector.Error as err:
            print(f"Error al seleccionar los datos: {err}")

    def pedido_archivos_historico(self):
        try:
            self.cursor = self.connection.cursor()

            sql = f"SELECT * FROM {self.table_historico}"
            self.cursor.execute(sql)
            
            rows= self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            
            return [dict(zip(columns, row)) for row in rows]
        
        except mysql.connector.Error as err:
            print(f"Error al seleccionar los datos: {err}")
    
    
    ########## FUNCION AUXILIARES PARA BUSCAR EN LA BASE DE DATOS ##########
    def existe_archivo(self, file_id):
        self.cursor = self.connection.cursor()
    
        sql = f"SELECT * FROM {self.table_inv} WHERE id=%s"
        self.cursor.execute(sql, (file_id,))
        
        result= self.cursor.fetchall()
        
        return bool(len(result))

    def existe_archivo_historico(self, file_id):
        self.cursor = self.connection.cursor()
    
        sql = f"SELECT * FROM {self.table_historico} WHERE id=%s"
        self.cursor.execute(sql, (file_id,))
        
        result= self.cursor.fetchall()
        
        return bool(len(result))

    def fue_modificado(self, file_id, file_last_modified_date):
        
        sql= f"SELECT fecha_ultima_modificacion FROM {self.table_inv} WHERE id=%s"
        self.cursor.execute(sql, (file_id,))
        
        ultima_modificacion=self.cursor.fetchone()[0]
        
        return file_last_modified_date > ultima_modificacion 



    ########## FUNCIONES DE UPDATES ##########
    def update_last_modified_date(self, file_id, file_modified_time):
        self.cursor = self.connection.cursor()
        
        sql= f"UPDATE {self.table_inv} SET fecha_ultima_modificacion=%s WHERE id=%s"
        values= (file_modified_time, file_id)
    
        self.cursor.execute(sql, values)
        self.connection.commit()

    def update_handler_visibility(self, file_id, file_modified_time):
        self.cursor = self.connection.cursor()
        new_visibility= "privado"
        was_public= 1
        
        sql1= f"UPDATE {self.table_inv} SET visibility=%s WHERE id=%s"
        values= (new_visibility, file_id)
        self.cursor.execute(sql1, values)
        
        sql2= f"UPDATE {self.table_inv} SET fecha_ultima_modificacion=%s WHERE id=%s"
        values= (file_modified_time, file_id)
        self.cursor.execute(sql2, values)
        
        sql3= f"UPDATE {self.table_inv} SET was_public=%s WHERE id=%s"
        values= (was_public, file_id)        
        self.cursor.execute(sql3, values)

        self.connection.commit()

    def update_archivo_historico(self, file_id, file_modified_time):
        self.cursor = self.connection.cursor()
        
        sql= f"UPDATE {self.table_historico} SET fecha_ultima_modificacion=%s WHERE id=%s"
        values= (file_modified_time, file_id) 
        self.cursor.execute(sql, values)
        self.connection.commit()
