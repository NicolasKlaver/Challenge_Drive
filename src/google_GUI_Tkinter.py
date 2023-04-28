import tkinter as tk
from tkinter import ttk
from google_DriveAPI import GoogleDriveAPI
from google_Database import Database
from google_DriveInventory import GoogleDriveInventory


class App:
    def __init__(self, root):
        self.driveAPI = GoogleDriveAPI()
        self.db= Database(user="root", password="root", host="localhost")
        self.driveINV = GoogleDriveInventory()
        
        # Definimos el objeto raíz de la aplicación y estableciendo el título de la ventana.
        self.root = root
        self.root.title("Challenge Docs en Drive Publico")
        
        self.crear_ventana()
        self.crear_boton_conexion()
        self.crear_boton_listar_archivos()
        self.crear_pestañas()
    
    ########## FUNCIONES PARA CREAR LOS GRAFICOS ##########
    def crear_ventana(self):
        # Creando un objeto Canvas que nos permitirá dibujar componentes gráficos en la ventana 
        # y lo estamos empaquetando dentro de la ventana raíz.
        self.canvas = tk.Canvas(self.root, height=150, width=150)
        self.canvas.pack()
        self.root.configure(bg='#3399FF')

        # Creando un objeto Label que nos permitirá mostrar un texto en la ventana.
        # create_window: tamaño y posición dentro del Canvas
        self.label = tk.Label(self.root, text="Bienvenido al Inventario de Google Drive")
        self.label.config(font=("Arial", 30), bg='#3399FF')
        self.canvas.create_window(100, 25, window= self.label)

    def crear_pestañas(self):
        # Creando un objeto Notebook que nos permitirá tener varias pestañas en la ventana.
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack()

        # Creamos la primera pestaña
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Tabla Inventario")
        self.crear_arbol_inventario()
       
        # Creamos la segunda pestaña
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="Tabla Publico - Historico")
        self.crear_arbol_historico() 
               
    def crear_boton_conexion(self):
            # Button que nos permitirá conectar a la API de Google Drive
            # self.connect_to_google_drive es la acción a ejecutar cuando el botón sea presionado.
        self.button_conn = tk.Button(text="Conectar a Google Drive", command=self.connect_to_google_drive)
        
        # configuramos la posición del botón dentro del Canvas utilizando el método create_window
        self.canvas.create_window(100, 100, window=self.button_conn)
        self.button_conn.configure(bg="#FFE4C9")  
    
    def crear_boton_listar_archivos(self):
        self.button_listar = tk.Button(text="Listar Archivos",  command=self.list_google_drive_files)
        # configuramos la posición del botón dentro del Canvas utilizando el método create_window
        self.canvas.create_window(100, 130, window=self.button_listar)
    
    def crear_arbol_inventario(self):
        # Crear el cuadro de la tabla
        self.tree = ttk.Treeview(self.tab1)
        self.tree.pack()
        # Agregar encabezados de columna
        self.tree['columns'] = ('id','name','extension','owner','visibility','last_modified_date','was_public')
        self.tree.heading('id', text='file_id')
        self.tree.column('id', width=50, minwidth=50)
        self.tree.heading('name', text='name')
        self.tree.column('name', width=300, minwidth=300)
        self.tree.heading('extension', text='extension')
        self.tree.column('extension', width=300, minwidth=300)
        self.tree.heading('owner', text='Owner')
        self.tree.column('owner', width=100, minwidth=100)
        self.tree.heading('visibility', text='visibility')
        self.tree.column('visibility', width=100, minwidth=100)     
        self.tree.heading('last_modified_date', text='last_modified_date')
        self.tree.column('last_modified_date', width=100, minwidth=100)
        self.tree.heading('was_public', text='was_public')
        self.tree.column('was_public', width=100, minwidth=100)
    
    def crear_arbol_historico(self):
        # Crear el cuadro de la tabla
        self.tree = ttk.Treeview(self.tab2)
        self.tree.pack()
        # Agregar encabezados de columna
        self.tree['columns'] = ('id','name','extension','owner','last_modified_date')
        self.tree.heading('id', text='file_id')
        self.tree.column('id', width=50, minwidth=50)
        self.tree.heading('name', text='name')
        self.tree.column('name', width=300, minwidth=300)
        self.tree.heading('extension', text='extension')
        self.tree.column('extension', width=300, minwidth=300)
        self.tree.heading('owner', text='Owner')
        self.tree.column('owner', width=100, minwidth=100)
        self.tree.heading('last_modified_date', text='last_modified_date')
        self.tree.column('last_modified_date', width=100, minwidth=100)


    ########## FUNCION PARA LOS BOTONES ##########       
    def connect_to_google_drive_and_database(self):
        #Conectar a Google Drive y listar los archivos
        self.driveAPI.connect()
        print("\nConectado a Google Drive - desde Tkinter\n")
        
        #Me conecto a MySQL
        self.db.open_connection()
        #Creo y selecciono una Base de Datos
        self.db.create_database("Inventario_Drive")
        self.db.select_database("Inventario_Drive")
        
        owner= self.drive_API.get_authenticated_user()
        nombre_inventario= "Inventario_" + owner
        nombre_inventario_historico= "Historico_" + owner
        #Creo las tablas 
        self.db.create_table_inventario(nombre_inventario)
        self.db.table_inv(nombre_inventario)
        self.db.create_table_historico(nombre_inventario_historico)
        self
    
    ##Aca deberia relacionarse con google_DriveInventory
    def list_google_drive_files(self):
        #files= self.driveAPI.get_files()
        self.driveINV.handler_files()
        
        ################# Para añadir deberia haber otra funcion
        #self.add_table_inventario(files)
        #self.add_table_historico(files)


    ########## FUNCION PARA AGREGAR INFORMACION A LA TABLA ##########
    def add_table_inventario(self, files):
        # Obtener la lista de archivos de la API de Google Drive
      
        # Agregar cada archivo como una fila en la tabla
        for file in files:
            self.tree.insert('', 'end', values=(file['id'], 
                                                file['name'], 
                                                file['extension'], 
                                                file['owner'], 
                                                file['visibility'], 
                                                file['modified_time'], 
                                                file['was_public']))
             
    def add_table_historico(self, files):
    # Agregar cada archivo como una fila en la tabla
        for file in files:
            self.tree.insert('', 'end', values=(file['id'], 
                                                file['name'], 
                                                file['extension'], 
                                                file['owner'], 
                                                file['modified_time']))
    

