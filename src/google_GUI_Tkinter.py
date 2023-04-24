import tkinter as tk
#import os.path
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google_DriveAPI import GoogleDriveAPI


class App:
    def __init__(self, root):
        self.driveAPI = GoogleDriveAPI()
        
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

        self.crear_boton_conexion()
        self.crear_boton_listar_archivos()
        
    def crear_boton_conexion(self):
            # Creamos un objeto Button que nos permitirá conectar a la API de Google Drive
            # self.connect_to_google_drive es la acción a ejecutar cuando el botón sea presionado.
        self.button_conn = tk.Button(text="Conectar a Google Drive", 
                                    command=self.connect_to_google_drive)
        # configuramos la posición del botón dentro del Canvas utilizando el método create_window
        self.canvas.create_window(250, 100, window=self.button_conn)
        
    def crear_boton_listar_archivos(self):
        self.button_listar = tk.Button(text="Listar Archivos", 
                                    command=self.list_google_drive_files)
        # configuramos la posición del botón dentro del Canvas utilizando el método create_window
        self.canvas.create_window(450, 100, window=self.button_listar)
    
    def connect_to_google_drive(self):
        #Conectar a Google Drive y listar los archivos
        self.driveAPI.connect()
        print("\nConectado a Google Drive - desde Tkinter\n")
                
    def list_google_drive_files(self):
        files= self.driveAPI.get_files()
        print(files)


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()

