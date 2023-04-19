from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from mysql.connector import connect
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os



####### Ejemplos de como conectarse a la base de datos
mydb = mysql.connector.connect(
  host="localhost",
  user="tu_usuario",
  password="tu_contraseña",
  database="nombre_de_la_base_de_datos"
)

# Creo la tabla
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE archivos (nombre_archivo VARCHAR(255), extension VARCHAR(10), propietario VARCHAR(255), visibilidad VARCHAR(10), fecha_ultima_modificacion VARCHAR(50))")

## Ejemplo de como subir un archivo
archivo = ("archivo.txt", "txt", "usuario1", "privado", "2022-01-01")
sql = "INSERT INTO archivos (nombre_archivo, extension, propietario, visibilidad, fecha_ultima_modificacion) VALUES (%s, %s, %s, %s, %s)"
mycursor.execute(sql, archivo)
mydb.commit()

#############################################################################################
# Obtener una lista de todos los archivos en la unidad de Drive del usuario
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

credentials = Credentials.from_authorized_user_info(user_info)
service = build('drive', 'v3', credentials=credentials)

results = service.files().list(
    pageSize=10, fields="nextPageToken, files(id, name)").execute()
items = results.get('files', [])
if not items:
    print('No files found.')
else:
    print('Files:')
    for item in items:
        print(u'{0} ({1})'.format(item['name'], item['id']))

#############################################################################################
##Para cada archivo en la lista de resultados, consulta su configuración de visibilidad utilizando 
##la propiedad permissions de la respuesta de la API.
permissions = service.permissions().list(
    fileId=item['id']).execute()

# Si el archivo tiene una configuración de visibilidad public, cambia su configuración a private
# utilizando la función update() de permissions.
for permission in permissions.get('permissions', []):
    if permission['type'] == 'anyone' and permission['role'] == 'reader':
        permission['role'] = 'writer'
        permission['type'] = 'user'
        permission['emailAddress'] = permission['emailAddress'] # to prevent email to user when changing back to private
        permission_id = permission['id']
        permission = service.permissions().update(
            fileId=item['id'], permissionId=permission_id, body=permission).execute()
        break

# También es importante guardar el estado de la visibilidad en la tabla de la base de datos
# buscar el archivo en la tabla utilizando su nombre y actualizar el valor en la columna visibilidad.
sql = "UPDATE archivos SET visibilidad = %s WHERE nombre_archivo = %s"
val = ("privado", item['name'])
mycursor.execute(sql, val)
mydb.commit()

# Envía un correo electrónico al propietario del archivo 
import smtplib

sender_email = "tucorreoelectronico@gmail.com"
receiver_email = "correoelectronicodelpropietario@gmail.com"
password = "tu_contraseña"

message = """\
Subject: Visibilidad de archivo cambiada

Hola,

La visibilidad de tu archivo {} ha sido cambiada a privado.

Saludos,
""".format(item['name'])

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)





############### CREO Y ME CONECTO A LA BASE DE DATOS
import mysql.connector

# Conexión a la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="username",
    password="password",
    database="database_name"
)

# Cursor
cursor = db.cursor()

# Crear tabla
cursor.execute("""
CREATE TABLE IF NOT EXISTS archivos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    extension VARCHAR(10) NOT NULL,
    owner VARCHAR(255) NOT NULL,
    visibilidad VARCHAR(10) NOT NULL,
    fecha_modificacion DATETIME NOT NULL,
    historico BOOLEAN NOT NULL DEFAULT FALSE
)
""")

# Cerrar conexión
db.close()



