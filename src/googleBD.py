import mysql.connector
import json
import datetime


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
    
    def insert_data(self, table_name, data):
        try:
            # Cargar los datos JSON en un objeto Python
            data_json= json.dumps(data)
            data_dict = json.loads(data_json)
        
            # Crear el cursor
            self.cursor = self.connection.cursor()


            # Ejecutar la consulta para cada conjunto de datos en la lista
            for item in data_dict:
                # Construir la consulta SQL
                sql = """INSERT INTO Inventario 
                    (name, extension, owner, visibility, fecha_ultima_modificacion, was_public)
                    VALUES (%s, %s, %s, %s, %s, %s)"""

            
                # Convertir el valor de was_public a un booleano
                was_public = 1 if item.get('visibility', '') == 'publico' else 0
                #print("Imprimo el valor de visibility: ", item.get('visibility', ''))
               # print("Imprimo el valor de was_public: ", was_public)
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
        

db = Database(host="localhost", user="root", password="root")
db.open_connection()
#db.create_database("mydatabaseTest")
db.select_database("mydatabaseTest") 
#db.create_table("Inventario")

data= [
  {
    "name": "documento1",
    "extension": "pdf",
    "owner": "usuario1@gmail.com",
    "visibility": "privado",
    "fecha_ultima_modificacion": "2022-04-19 13:00:00"
  },
  {
    "name": "imagen1",
    "extension": "png",
    "owner": "usuario2@gmail.com",
    "visibility": "publico",
    "fecha_ultima_modificacion": "2022-04-18 10:30:00"
  },
  {
    "name": "documento2",
    "extension": "docx",
    "owner": "usuario3@gmail.com",
    "visibility": "publico",
    "fecha_ultima_modificacion": "2022-04-17 14:45:00"
  }
    ]

#db.insert_data("Inventario", data)

db.update_visibility(table_name="Inventario")


db.close_connection()