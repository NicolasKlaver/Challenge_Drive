from googleArchivos import GoogleDriveInventory
from googleBD import Database
import tkinter as tk
import os.path
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class GoogleDriveAPI:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/drive']
        #SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
        self.creds = None
    
    def authenticate(self):
        if not creds or not creds.valid:
            # Si el token existe pero está vencido, se actualiza utilizando el refresh token.
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # Si no existe un token o está vencido y no se cuenta con el refresh token, se procede
                # a realizar la autenticación con el usuario.
                flow = InstalledAppFlow.from_client_secrets_file('credential_tkinter.json', SCOPES)
                creds = flow.run_local_server(port=0)
                
            # Una vez que se obtiene el token, se almacena en un archivo local para futuras consultas
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return creds
    
    def connect(self):
        # Conectar a Google Drive
        try:
            self.authenticate()
            self.service = build('drive', 'v3', credentials=self.creds)
            print("Conexión exitosa a Google Drive.")
        except HttpError as error:
            print(f"Se produjo un error al conectarse a Google Drive: {error}")
    
    def disconnect(self):
        # Desconectar de Google Drive
        self.service = None
        print("Desconexión exitosa de Google Drive.")
    
    def get_files(self):
        # Obtener los archivos de Google Drive
        try:
            results = self.service.files().list(
                q=query, fields="nextPageToken, files(id, name)").execute()
            items = results.get('files', [])
            return items
        except HttpError as error:
            print(f"Se produjo un error al obtener los archivos: {error}")
            return None
    
    def revoke_file_permission(self, file_id):
        # Revocar los permisos de un archivo en Google Drive
        try:
            self.service.permissions().delete(
                fileId=file_id, permissionId='anyoneWithLink').execute()
            print(f"Permisos revocados para el archivo con ID {file_id}")
        except HttpError as error:
            print(f"Se produjo un error al revocar los permisos del archivo con ID {file_id}: {error}")


    
    
    