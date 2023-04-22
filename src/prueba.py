from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------

#  La clase GoogleDriveFile representa un archivo de Google Drive y proporciona un método
# is_public para verificar si el archivo es público

class GoogleDriveFile:
    def __init__(self, file):
        self.id = file["id"]
        self.name = file["name"]
        self.created_time = file["createdTime"]
        self.modified_time = file["modifiedTime"]
        self.mime_type = file["mimeType"]
        self.owners = file["owners"]
        self.sharing_settings = file["sharingSettings"]

    def is_public(self):
        return self.sharing_settings["type"] == "anyone" and self.sharing_settings["role"] == "reader"
    

# Crea una clase MySQLConnector para conectarse a la base de datos MySQL:
    #Incluye un constructor para configurar las credenciales de acceso a la base de datos.
    # Incluye métodos para insertar o actualizar registros en la tabla de archivos de Google Drive.

#En este ejemplo, la clase MySqlConnector se encarga de conectarse a la base de datos MySQL y ejecutar consultas SQL.

#La clase MySqlConnector se inicializa con los datos necesarios para establecer la conexión con la base de datos (host, usuario, contraseña y nombre de la base de datos). Una vez que se establece la conexión, se utiliza el método execute_query para ejecutar una consulta SQL y devolver el resultado.

#El método execute_query toma dos argumentos: query es la consulta SQL que se va a ejecutar y params es una lista opcional de parámetros que se van a pasar a la consulta SQL.

#El método close_connection se encarga de cerrar la conexión con la base de datos.

import mysql.connector

class MySqlConnector:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def execute_query(self, query, params=None):
        cursor = self.connection.cursor()

        try:
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.fetchall()

        except mysql.connector.Error as error:
            print(f"An error occurred: {error}")
            self.connection.rollback()

        finally:
            cursor.close()

    def close_connection(self):
        self.connection.close() 
    

# Crea una clase GoogleDriveInventory para gestionar el inventario de archivos de Google Drive:    
    #Incluye un constructor para crear instancias de GoogleDriveAPI y MySQLConnector.
    # Incluye métodos para gestionar el inventario de archivos de Google Drive, 
    # como update_file para actualizar un archivo existente en la base de datos, 
    # insert_file para insertar un nuevo archivo en la base de datos y 
    # check_visibility para comprobar y cambiar la configuración de visibilidad de un archivo.
import datetime
import os
from googleDriveAPI import GoogleDriveAPI
from mysqlConnector import MySqlConnector

class GoogleDriveInventory:
    def __init__(self, credentials_file_path, db_host, db_user, db_password, db_name):
        self.drive_api = GoogleDriveAPI(credentials_file_path)
        self.db = MySqlConnector(db_host, db_user, db_password, db_name)

    def get_files_list(self):
        files_list = self.drive_api.get_files_list()
        return files_list

    def inventory_files(self):
        files_list = self.get_files_list()
        for file in files_list:
            file_id = file['id']
            file_name = file['name']
            file_extension = os.path.splitext(file_name)[1]
            file_owner = file['owners'][0]['emailAddress']
            file_visibility = file['visibility']
            file_modified_time = datetime.datetime.fromisoformat(file['modifiedTime'])

            # Check if the file is already in the inventory
            query = "SELECT * FROM files WHERE file_id = %s"
            params = (file_id,)
            result = self.db.execute_query(query, params)

            # If the file is not in the inventory, add it
            if len(result) == 0:
                query = "INSERT INTO files (file_id, file_name, file_extension, file_owner, file_visibility, file_modified_time) VALUES (%s, %s, %s, %s, %s, %s)"
                params = (file_id, file_name, file_extension, file_owner, file_visibility, file_modified_time)
                self.db.execute_query(query, params)

            # If the file is already in the inventory, update the modified time
            else:
                query = "UPDATE files SET file_modified_time = %s WHERE file_id = %s"
                params = (file_modified_time, file_id)
                self.db.execute_query(query, params)

            # If the file is public, make it private and send an email to the owner
            if file_visibility == 'anyoneCanView':
                self.drive_api.revoke_file_permission(file_id)
                subject = f"Change in visibility for file '{file_name}'"
                body = f"Your file '{file_name}' is no longer publicly visible."
                self.drive_api.send_email(file_owner, subject, body)

    def close_inventory(self):
        self.db.close_connection()

#En este ejemplo, la clase GoogleDriveInventory se encarga de inventariar los archivos de Google Drive y almacenarlos en una base de datos MySQL. Para hacer esto, utiliza la clase GoogleDriveAPI para obtener la lista de archivos de Google Drive y la clase MySqlConnector para realizar operaciones de lectura y escritura en la base de datos MySQL.

#La clase GoogleDriveInventory se inicializa con los datos necesarios para conectarse a la API de Google Drive y a la base de datos MySQL.

#El método get_files_list utiliza la clase GoogleDriveAPI para obtener la lista de archivos de Google Drive y devuelve esa lista.

#El método inventory_files recorre la lista de archivos de Google Drive y para cada archivo:

#Obtiene el ID del archivo, el nombre del archivo, la extensión del archivo, el propietario del archivo, la visibilidad del archivo y la fecha de mod


    
#Crea una clase GoogleDriveEmailNotifier para enviar correos electrónicos:
    # Incluye un constructor para configurar las credenciales de acceso al servicio de correo electrónico.
    # Incluye un método send_notification para enviar un correo electrónico al propietario 
    # de un archivo cuando se cambia la configuración de visibilidad de un archivo.
    
#En este ejemplo, la clase GoogleDriveEmailNotifier utiliza la biblioteca smtplib para enviar correos electrónicos mediante el protocolo SMTP. El método send_email acepta los parámetros to (destinatario), subject (asunto), message (cuerpo del mensaje) y attachment (opcionalmente, una ruta de archivo adjunto).

#Dentro del método, se crea un objeto MIMEMultipart que contiene la información del correo electrónico, y se utiliza la biblioteca email.mime para agregar el cuerpo del mensaje y, opcionalmente, el archivo adjunto.

#Luego, se utiliza la función smtplib.SMTP para conectarse al servidor SMTP de Gmail, y se utiliza el método starttls para cifrar la conexión. Luego, se utiliza el método login para autenticarse con la dirección de correo electrónico y la contraseña proporcionadas en el constructor. Finalmente, se utiliza el método sendmail para enviar el correo electrónico al destinatario especificado.
    
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

class GoogleDriveEmailNotifier:
    def __init__(self, email_address, password):
        self.email_address = email_address
        self.password = password

    def send_email(self, to, subject, message, attachment=None):
        msg = MIMEMultipart()
        msg['From'] = self.email_address
        msg['To'] = to
        msg['Subject'] = subject
        body = MIMEText(message)
        msg.attach(body)

        if attachment:
            with open(attachment, 'rb') as f:
                attach = MIMEApplication(f.read(),_subtype='pdf')
                attach.add_header('Content-Disposition','attachment',filename=str(attachment))
                msg.attach(attach)

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email_address, self.password)
            server.sendmail(self.email_address, to, msg.as_string())
            server.quit()
            print("Email sent successfully.")
        except Exception as e:
            print("Error sending email: ", str(e))
    



###################3

# En este ejemplo, la función load_dotenv carga automáticamente las variables de entorno desde el archivo .env en el entorno de ejecución del script. Luego, se pueden acceder a estas variables de entorno utilizando la función os.getenv.

from dotenv import load_dotenv
import os

load_dotenv()

database_host = os.getenv('DATABASE_HOST')
database_user = os.getenv('DATABASE_USER')
database_password = os.getenv('DATABASE_PASSWORD')
database_name = os.getenv('DATABASE_NAME')
gmail_user = os.getenv('GMAIL_USER')
gmail_password = os.getenv('GMAIL_PASSWORD')