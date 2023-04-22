# ---------------------------------------------------------------------------------------------
# Crea una clase GoogleDriveAPI para acceder a la API de Google Drive:
    # Incluye un constructor para configurar las credenciales de acceso a la API de Google Drive.
    # Incluye un método get_files para obtener una lista de archivos de Google Drive del usuario.
    
    


# Se encarga de conectarse a la API de Google Drive y obtener la lista de archivos
# Se inicializa con las credenciales de autenticación que se obtienen del archivo
# JSON descargado de la consola de desarrolladores de Google.
# Una vez autenticado, se utiliza el método build de googleapiclient.discovery
# para crear un objeto service que se utiliza para interactuar con la API de Google Drive.




from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build


class GoogleDriveApi:
    ##Solo recibe el path de las credenciales
    def __init__(self, credentials_path):
        self.credentials_path = credentials_path
        self.creds = None
        self.drive_service = None

    ##Se encarga de autorizar la conexión a la API de Google Drive
    def authorize(self):
        if self.creds is not None and self.creds.valid:
            return
        if self.creds is not None and self.creds.expired and self.creds.refresh_token:
            self.creds.refresh(Request())
            return
        flow = InstalledAppFlow.from_client_secrets_file(
            self.credentials_path,
            ['https://www.googleapis.com/auth/drive']
        )
        self.creds = flow.run_local_server(port=0)
    
    ## devuelve el servicio de Google Drive almacenado o crea uno nuevo
    def get_drive_service(self):
        if self.drive_service is not None:
            return self.drive_service
        self.authorize()
        self.drive_service = build('drive', 'v3', credentials=self.creds)
        return self.drive_service
    
    def list_files(self):
        try:
            drive_service = self.get_drive_service()
            query = "mimeType!='application/vnd.google-apps.folder' and trashed=false"
            files = drive_service.files().list(q=query).execute().get('files', [])
            return files
        except HttpError as error:
            print(f'An error occurred: {error}')
            return []
    
    
# PRUEBAS  
##google_drive_api = GoogleDriveApi('/path/to/credentials.json')
##drive_service = google_drive_api.get_drive_service()
##files = google_drive_api.list_files()