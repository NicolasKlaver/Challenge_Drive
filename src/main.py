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
