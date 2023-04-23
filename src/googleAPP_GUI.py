import tkinter as tk
import os.path
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request



class App:
    def __init__(self, root):
        # Definimos el objeto raíz de la aplicación y estableciendo el título de la ventana.
        self.root = root
        self.root.title("Lista de archivos de Google Drive")
        
        # Creando un objeto Canvas que nos permitirá dibujar componentes gráficos 
        # en la ventana y lo estamos empaquetando (con el método pack) dentro de la ventana raíz.
        self.canvas = tk.Canvas(self.root, height=500, width=500)
        self.canvas.pack()

        # Creando un objeto Label que nos permitirá mostrar un texto en la ventana.
        # Configuramos el tamaño de la fuente y la posición del Label dentro del Canvas
        # utilizando el método create_window.
        self.label = tk.Label(self.root, text="Bienvenido a la lista de archivos de Google Drive!")
        self.label.config(font=("Arial", 14))
        self.canvas.create_window(250, 25, window= self.label)

        # Creamos un objeto Button que nos permitirá conectar a la API de Google Drive
        # Asignamos la función self.connect_to_google_drive como acción a ejecutar cuando
        # el botón sea presionado.
        self.button = tk.Button(text="Conectar a Google Drive", command=self.connect_to_google_drive)
        # configuramos la posición del botón dentro del Canvas utilizando el método create_window
        self.canvas.create_window(250, 100, window=self.button)
    
    def authenticate_google_drive(self):
        #Autenticar la aplicación en Google Drive y obtener un token de acceso
        
        # Definimos los scopes (permisos) necesarios para la autenticación.
        # En este caso solo solicitamos permisos de lectura de los metadatos de los archivos.
        SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
        creds = None
        
        # Verificamos si ya existe un token de acceso válido en el sistema.
        if os.path.exists('token.json'):
            # Si el token ya existe, lo cargamos en la variable creds.
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        # Si no existe, se procede a obtener uno nuevo mediante la autenticación del usuario.
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
    
    def connect_to_google_drive(self):
        #Conectar a Google Drive y listar los archivos
        self.list_google_drive_files()
        
    def list_google_drive_files(self):
        #Listar los archivos de Google Drive
        try:
            # obtiene las credenciales de autenticación necesarias para acceder a los archivos de Google Drive
            creds = self.authenticate_google_drive()
            # se utiliza la función build para construir un objeto service que permite interactuar con la API de Google Drive.
            #  Se especifica que se desea trabajar con la versión 3 de la API, y se proporcionan las credenciales de autenticación
            service = build('drive', 'v3', credentials=creds)
            
            #llama al método files().list(), para obtener una lista de los archivos de Google Drive
            results = service.files().list(
                # solo se desea obtener el nextPageToken y los campos id y name de cada archivo.
                pageSize=10, fields="nextPageToken, files(id, name)").execute()
            
            # se extrae la lista de archivos (items) de los resultados obtenidos en la línea anterior. 
            items = results.get('files', [])
            if not items:
                # Si no hay archivos, se devuelve una lista vacía.
                print('No se encontraron archivos.')
            else:
                # Si hay archivos en la lista, se itera sobre cada uno de ellos e imprime su nombre y su ID en la consola.
                print(items)
                #for item in items:
                 #   print(u'{0} ({1})'.format(item['name'], item['id']))
        # Si se produce un error al intentar acceder a la API de Google Drive, se captura y se imprime en la consola un mensaje de error.
        except HttpError as error:
            print('Se produjo un error: {0}'.format(error))
    

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()


"""
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

"""
