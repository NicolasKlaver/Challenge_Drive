#from google_DriveInventory import GoogleDriveInventory
#from google_Database import Database
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
#from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class GoogleDriveAPI:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/drive']
        self.creds = None
    
    def authenticate(self):
        if not self.creds or not self.creds.valid:
            # Si el token existe pero está vencido, se actualiza utilizando el refresh token.
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                # Si no existe un token o está vencido y no se cuenta con el refresh token, se procede
                # a realizar la autenticación con el usuario.
                flow = InstalledAppFlow.from_client_secrets_file('C:/Users/HP/Downloads/INTEGRACION/credential_tkinter.json', self.SCOPES)## SCOPES
                self.creds = flow.run_local_server(port=0)
                
            # Una vez que se obtiene el token, se almacena en un archivo local para futuras consultas
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())
        return self.creds
    
    def connect(self):
        try:
            self.authenticate()
            self.service = build('drive', 'v3', credentials=self.creds)
            print("Conexión exitosa a Google Drive - Desde google_DriveAPI.")
        except HttpError as error:
            print(f"Se produjo un error al conectarse a Google Drive: {error}")
    
    def disconnect(self):
        # Desconectar de Google Drive
        self.service = None
        print("Desconexión exitosa de Google Drive.")
    
    def revoke_file_permission(self, file_id):
       pass
    """
        # Revocar los permisos de un archivo en Google Drive
        try:
            self.service.permissions().delete(
                fileId=file_id, permissionId='anyoneWithLink').execute()
            print(f"Permisos revocados para el archivo con ID {file_id}")
        except HttpError as error:
            print(f"Se produjo un error al revocar los permisos del archivo con ID {file_id}: {error}")
    """
    
    def get_files(self):
        try:
            # Definir los campos que queremos obtener para cada archivo
            fields = "nextPageToken, files(id, name, mimeType, owners(emailAddress), modifiedTime)"
            #fields = "nextPageToken, files(id, name, mimeType, owners(emailAddress), visibility, modifiedTime)"

            # Obtener los archivos de Google Drive
            results = self.service.files().list(q=None, fields=fields, pageSize=3).execute()
            print("\n\nG-API: Imprimo Results: ", results)
            items = results.get('files', [])
            print("\n\nG-API: Imprimo items: ", items)
            # Procesar la lista de archivos y extraer los campos necesarios
            files = []
            for item in items:
                # Obtener la extensión del archivo a partir del tipo MIME
                extension = item['mimeType'].split('/')[-1]
                # Obtener el nombre del propietario
                owner = item['owners'][0]['emailAddress']
                # Agregar un diccionario con los campos que nos interesan a la lista de archivos
                files.append({
                    'id': item['id'],
                    'name': item['name'],
                    'extension': extension,
                    'owner': owner,
                    #'visibility': item['visibility'],
                    'visibility': "publico",
                    'modified_time': item['modifiedTime']
                })
                print("\n\nG-API: Imprimo una vuelta de files: ", files)
            print("\n\nImprimo todo files: ", files)
            return files
    
        except HttpError as error:
            print(f"Se produjo un error al obtener los archivos: {error}")
            return None
        

        
    



    
    
    