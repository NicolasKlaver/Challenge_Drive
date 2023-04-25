import tkinter as tk
from tkinter import ttk

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
        self.canvas = tk.Canvas(self.root, height=300, width=300)
        self.canvas.pack()

        # Creando un objeto Label que nos permitirá mostrar un texto en la ventana.
        # Configuramos el tamaño de la fuente y la posición del Label dentro del Canvas
        # utilizando el método create_window.
        self.label = tk.Label(self.root, text="Bienvenido a la lista de archivos de Google Drive!")
        self.label.config(font=("Arial", 14))
        self.canvas.create_window(250, 25, window= self.label)

        
        self.crear_arbol()
        self.crear_boton_conexion()
        self.crear_boton_listar_archivos()
        
    def populate_table(self, files):
        # Obtener la lista de archivos de la API de Google Drive
      
        # Agregar cada archivo como una fila en la tabla
        for file in files:
            #self.tree.insert('', 'end', values=(file['id'], file['name'], file['extension'], file['owner'], file['visibility'], file['modified_time'], file['was_public']))
            self.tree.insert('', 'end', values=(file['id'], file['name'], file['extension'], file['owner'], file['modified_time']))
    
    def crear_boton_conexion(self):
            # Creamos un objeto Button que nos permitirá conectar a la API de Google Drive
            # self.connect_to_google_drive es la acción a ejecutar cuando el botón sea presionado.
        self.button_conn = tk.Button(text="Conectar a Google Drive", 
                                    command=self.connect_to_google_drive)
        # configuramos la posición del botón dentro del Canvas utilizando el método create_window
        self.canvas.create_window(100, 100, window=self.button_conn)
        
    def crear_boton_listar_archivos(self):
        self.button_listar = tk.Button(text="Listar Archivos", 
                                    command=self.list_google_drive_files)
        # configuramos la posición del botón dentro del Canvas utilizando el método create_window
        self.canvas.create_window(100, 130, window=self.button_listar)
    
    def crear_arbol(self):
        # Crear el cuadro de la tabla
        self.tree = tk.ttk.Treeview(root)
        self.tree.pack()
        # Agregar encabezados de columna
        #self.tree['columns'] = ('id','name','extension','owner','visibility','last_modified_date','was_public')
        self.tree['columns'] = ('id','name','extension','owner','last_modified_date')
        self.tree.heading('id', text='id del archivo')
        self.tree.heading('name', text='Nombre del archivo')
        self.tree.heading('extension', text='extension del archivo')
        self.tree.heading('owner', text='Owner')
        #self.tree.heading('visibility', text='Visibility')
        self.tree.heading('last_modified_date', text='last_modified_date')
        #self.tree.heading('was_public', text='was_public')
    
    def connect_to_google_drive(self):
        #Conectar a Google Drive y listar los archivos
        self.driveAPI.connect()
        print("\nConectado a Google Drive - desde Tkinter\n")
                
    def list_google_drive_files(self):
        files= self.driveAPI.get_files()
        print(files)
        self.populate_table(files)


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()

