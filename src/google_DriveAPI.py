from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
import pickle
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from logger import Logger
from cifrado import Cypher
import json


class GoogleDriveAPI:
    """
    Clase para conectarse a la API de Google Drive y obtener los archivos que se encuentran en la carpeta compartida.

    Returns:
        _type_: _description_
    """
    ########## FUNCION DE INICIALIZACION ##########
    def __init__(self):
        """
        Inicializa la clase DriveAPI y define los scopes de acceso para la autenticación de la API de Google Drive.
        
        Args: Ninguno
            
        Returns: Ninguno
        """
        self.SCOPES = ['https://www.googleapis.com/auth/drive']
        #self.SCOPES =['https://www.googleapis.com/auth/drive.metadata.readonly', 'https://www.googleapis.com/auth/drive']
        self.creds = None
        self.logger = Logger().get_logger()
        #self.logger = None
    
    
    ########## FUNCIONES PARA CONECTARSE ##########
    def authenticate(self):
        """
        Autenticar a la aplicación para acceder a la API de Google Drive. 
        Si existe un token previamente guardado y no ha expirado, se utiliza ese token. 
        En caso contrario, se solicita la autenticación del usuario y se guarda el token en un archivo local.
        
        Args: None
        
        Returns:
            Credenciales de autenticación para acceder a la API de Google Drive.
        """
        
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        
        if not self.creds or not self.creds.valid:
            # Si el token existe pero está vencido, se actualiza utilizando el refresh token.
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                # Si no existe un token o está vencido y no se cuenta con el refresh token, se procede
                # a realizar la autenticación con el usuario.
                
                # Creo el archivo de las credenciales
                self.desencriptar_credenciales()

                flow = InstalledAppFlow.from_client_secrets_file("credenciales.json", self.SCOPES)
                self.creds = flow.run_local_server(port=0)
                
                # Eliminar el archivo temporal de credenciales
                self.eliminar_credenciales_desencriptadas()
                
            
            # Una vez que se obtiene el token, se almacena en un archivo local para futuras consultas
            #with open('token.json', 'w') as token:
            #    token.write(self.creds.to_json())
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)
             
        return self.creds
    
    def connect(self):
        """
        Conectarse a la API de Google Drive. 
        Si la autenticación es exitosa, se guarda el objeto del servicio de Google Drive en la variable 'self.service'.
        Args: None
        
        Returns: None
        """
        try:
            self.authenticate()
            self.service = build('drive', 'v3', credentials=self.creds)
            
            print("Conexión exitosa a Google Drive - Desde google_DriveAPI.")
            self.logger.info("Conexión exitosa a Google Drive - Desde google_DriveAPI.")
            
        except HttpError as error:
            print(f"Se produjo un error al conectarse a Google Drive: {error}")
            self.logger.error(f"Error al conectar a la base de datos: {error}")
    
    def disconnect(self):
        """
        Desconectar de la API de Google Drive. Se establece la variable 'self.service' en None.
        
        Args: None
        
        Returns: None
        """
        
        # Desconectar de Google Drive
        self.service = None
        print("Desconexión exitosa de Google Drive.")
        self.logger.info("Desconexión exitosa de Google Drive.")
    
    def desencriptar_credenciales(self):
        cipher = Cypher()
        datos_cred = cipher.decrypt(flag_cred=1, flag_env=0)
        
        # Creo un archivo temporalmente
        with open("credenciales.json", "w") as f:
            json.dump(datos_cred, f)
    
    def eliminar_credenciales_desencriptadas(self):
        os.remove("credenciales.json")
    
    ########## FUNCIONES PARA OBTENER ARCHIVOS ##########
    
    def get_files(self):
        """
        Obtener los archivos de Google Drive que cumplan con ciertos criterios de búsqueda. 
        Los campos que se obtienen para cada archivo son: id, name, mimeType, owners, permissions y modifiedTime.
        
        Args: None
        
        Return (list):
            Lista de archivos que cumplen con los criterios de búsqueda.
        """
        
        try:
            # Definir los campos que queremos obtener para cada archivo
            fields = "nextPageToken, files(id, name, mimeType, owners(emailAddress), permissions, modifiedTime)"
            query = "trashed = false and mimeType='application/pdf' "# Para pruebas
            #query= "trashed = false"
            # Obtener los archivos de Google Drive
            results = self.service.files().list(q=query, fields=fields, pageSize=3).execute() # Para pruebas
            
            items = results.get('files', [])
            # Procesar la lista de archivos y extraer los campos necesarios
            files = []
            for item in items:
                # Obtener la extensión del archivo a partir del tipo MIME
                extension = item['mimeType'].split('/')[-1]
                # Obtener el nombre del propietario
                owner = item['owners'][0]['emailAddress']
                
                # Obtener la lista de permisos del archivo
                permissions = item.get('permissions', [])
                #is_public = self.es_publico(permissions)
                is_public = self.es_publico(permissions)
        
                # Agregar un diccionario con los campos que nos interesan a la lista de archivos
                files.append({
                    'id': item['id'],
                    'name': item['name'],
                    'extension': extension,
                    'owner': owner,
                    'visibility': 'publico' if is_public else 'privado',
                    'modified_time': item['modifiedTime']
                })
            print(files)
            self.logger.info("Se listaron los archivos de Google Drive con exito.")
            return files
    
        except HttpError as error:
            print(f"Se produjo un error al obtener los archivos: {error}")
            self.logger.error(f"Se produjo un error al obtener los archivos: {error}")
            return None
    
 
    def get_all_files(self):
        """
        Obtener los archivos de Google Drive que cumplan con ciertos criterios de búsqueda. 
        Los campos que se obtienen para cada archivo son: id, name, mimeType, owners, permissions y modifiedTime.

        Args: None

        Return (list):
            Lista de archivos que cumplen con los criterios de búsqueda.
        """
        try:
            # Definir los campos que queremos obtener para cada archivo
            fields = "nextPageToken, files(id, name, mimeType, owners(emailAddress), permissions, modifiedTime)"
            query = "trashed = false and 'me' in owners"
            all_files = []
            page_token = None
            
            while True:
                results = self.service.files().list(q=query, fields=fields, pageToken=page_token).execute()
                items = results.get('files', [])
                all_files.extend(items)
                page_token = results.get('nextPageToken')
                if not page_token:
                    break
            # Procesar la lista de archivos y extraer los campos necesarios
            files = []
            for item in all_files:
                # Obtener la extensión del archivo a partir del tipo MIME
                extension = item['mimeType'].split('/')[-1]
                # Obtener el nombre del propietario
                owner = item['owners'][0]['emailAddress']

                # Obtener la lista de permisos del archivo
                permissions = item.get('permissions', [])
                # is_public = self.es_publico(permissions)
                is_public = self.es_publico(permissions)

                # Agregar un diccionario con los campos que nos interesan a la lista de archivos
                files.append({
                    'id': item['id'],
                    'name': item['name'],
                    'extension': extension,
                    'owner': owner,
                    'visibility': 'publico' if is_public else 'privado',
                    'modified_time': item['modifiedTime']
                })
            print(files)
            self.logger.info("Se listaron los archivos de Google Drive con exito.")
            return files
        except HttpError as error:
            print(f"Se produjo un error al obtener los archivos: {error}")
            self.logger.error(f"Se produjo un error al obtener los archivos: {error}")
            return None
   
    
    def test_visibility_file(self, file_id):
        """
        Obtener un archivo de Google Drive por su ID.

        Args:
            file_id (str): ID del archivo que se desea obtener.

        Return:
            Un diccionario con la información del archivo, incluyendo su ID, nombre, tipo MIME,
            propietario, permisos y fecha de modificación. Si no se encuentra el archivo, devuelve None.
        """
        
        try:
            # Definir los campos que queremos obtener para el archivo
            fields = "id, permissions"
            
            # Obtener el archivo de Google Drive
            file = self.service.files().get(fileId=file_id, fields=fields).execute()
                        
            # Obtener la lista de permisos del archivo
            permissions = file.get('permissions', [])
            for perm in permissions:
                if perm.get('id', '') == 'anyoneWithLink':
                    return "publico"

            return 'privado'

        except HttpError as error:
            print(f"Se produjo un error al obtener el archivo: {error}")
            self.logger.error(f"Se produjo un error al obtener el archivo: {error}")
            return None
    
    def test_list_one_file(self):
        """
        Obtener los archivos de Google Drive que cumplan con ciertos criterios de búsqueda. 
        Los campos que se obtienen para cada archivo son: id, name, mimeType, owners, permissions y modifiedTime.
        
        Args: None
        
        Return (list):
            Lista de archivos que cumplen con los criterios de búsqueda.
        """
        
        try:
            # Definir los campos que queremos obtener para cada archivo
            fields = "nextPageToken, files(id, name, mimeType, owners(emailAddress), permissions, modifiedTime)"
            query = "trashed = false and mimeType='application/pdf' "

            # Obtener los archivos de Google Drive
            results = self.service.files().list(q=query, fields=fields, pageSize=2).execute()
            items = results.get('files', [])
            # Procesar la lista de archivos y extraer los campos necesarios
            files = []
            for item in items:
                # Obtener la extensión del archivo a partir del tipo MIME
                extension = item['mimeType'].split('/')[-1]
                # Obtener el nombre del propietario
                owner = item['owners'][0]['emailAddress']
                
                # Obtener la lista de permisos del archivo
                permissions = item.get('permissions', [])
                #is_public = self.es_publico(permissions)
                is_public = False
                for perm in permissions:
                    if  perm.get('id', '') == 'anyoneWithLink':
                        is_public = True
                        break 
        
                # Agregar un diccionario con los campos que nos interesan a la lista de archivos
                files.append({
                    'id': item['id'],
                    'name': item['name'],
                    'extension': extension,
                    'owner': owner,
                    'visibility': 'publico' if is_public else 'privado',
                    'modified_time': item['modifiedTime']
                })
            print(files)
            return files
    
        except HttpError as error:
            print(f"Se produjo un error al obtener los archivos: {error}")
            return None    
    
    ########## FUNCION PARA CAMBIAR LA VISIBILIDAD ##########    
    def remove_public_visibility(self, file_id):
        """
        Revocar los permisos públicos de un archivo de Google Drive, de manera que solo pueda ser accedido por los 
        usuarios con permisos explícitos. 
        
        Args:
            file_id(str): ID del archivo de Google Drive.
            
        Returns: None
        """
        # Revocar los permisos de un archivo en Google Drive
        try:
            self.service.permissions().delete(fileId= file_id, permissionId='anyoneWithLink').execute()
            print(f"Permisos revocados para el archivo con ID {file_id}")
            self.logger.info(f"Permisos revocados para el archivo con ID {file_id}")
            
        except HttpError as error:
            print(f"Se produjo un error al revocar los permisos del archivo con ID {file_id}: {error}")
            self.logger.error(f"Se produjo un error al revocar los permisos del archivo con ID {file_id}: {error}")
     
    def get_last_modified_date(self, file_id):
        """
        Obtener la fecha de última modificación de un archivo de Google Drive.
        
        Args:
            file_id (str): ID del archivo de Google Drive.
        
        Returns:
            Fecha de última modificación del archivo de Google Drive.
        """
        try:
            modified_info = self.service.files().get(fileId= file_id, fields='modifiedTime').execute()
            return modified_info['modifiedTime']
        
        except HttpError as error:
            print(f"Se produjo un error al obtener la información del usuario autenticado: {error}")
            self.logger.error(f"Se produjo un error al obtener la información del usuario autenticado: {error}")
            return None 
    
    def get_authenticated_user(self):
        """
        Obtener la dirección de correo electrónico del usuario autenticado en Google Drive.
        
        Args: None
        
        Return (str): Dirección de correo electrónico del usuario autenticado en Google Drive.
        """
        
        try:
            user_info = self.service.about().get(fields='user(emailAddress)').execute()
            return user_info['user']['emailAddress']
        
        except HttpError as error:
            print(f"Se produjo un error al obtener la información del usuario autenticado: {error}")
            self.logger.error(f"Se produjo un error al obtener la información del usuario autenticado: {error}")
            return None 
    
    def es_publico(self, permissions):
        """
        Verificar si un archivo de Google Drive es público o no, en base a la lista de permisos del archivo.
        
        Args:
            permissions(list): Lista de permisos del archivo de Google Drive.
        
        Returns:
            True si el archivo es público (cualquiera con el enlace puede acceder), False en caso contrario.
        """
        
        # Buscar si hay algún permiso
        for perm in permissions:
            print("Imprimo el permiso:", perm)
            if  perm.get('id', '') == 'anyoneWithLink':
                return True  
        return False


