import tkinter as tk
import datetime
from tkinter import ttk
import tkinter.messagebox as messagebox
from google_DriveAPI import GoogleDriveAPI
from google_Database import Database
from google_DriveInventory import GoogleDriveInventory
from dotenv import load_dotenv
import os

"""def salirAplicacion():
	valor=messagebox.askquestion("Salir","¿Está seguro que desea salir de la Aplicación?")
	if valor=="yes":
		root.destroy()"""

class App:
    def __init__(self, root):
        """
        Inicializa la interfaz de usuario y todas las variables necesarias para conectarse con la base de datos y con la API de Google Drive.

        Args:
            root: Objeto Tk que representa la ventana principal de la aplicación.
        
        Returns: None
        """
        
        self.driveAPI = GoogleDriveAPI()
        
        # Carga las variables de entorno desde el archivo .env
        load_dotenv('config/.env')
        # Obtiene las credenciales de la base de datos desde las variables de entorno
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")
        
        self.db= Database(db_user, db_password, db_host)
        self.driveINV = GoogleDriveInventory(self.db, self.driveAPI)

        
        # Definimos el objeto raíz de la aplicación y estableciendo el título de la ventana.
        self.root = root
        self.root.title("Challenge Docs en Drive Publico")
        self.root.configure(background="#7cdaf9")
        
        self.crear_ventana_bienvenida()
        self.crear_boton_inicio()
        self.crear_pestañas()
    
    ########## FUNCIONES PARA CREAR LOS GRAFICOS ##########
    def crear_ventana_bienvenida(self):
        """
        Crea la ventana principal de la aplicación y define la etiqueta de bienvenida.

        :return: None
        """
        
        # Creando un objeto Canvas que nos permitirá dibujar componentes gráficos en la ventana 
        # y lo estamos empaquetando dentro de la ventana raíz.
        # Crear el rectángulo de bienvenida
        self.label = tk.Label(self.root, 
                              text="Bienvenidos al Inventario de Google Drive", 
                              font=("Franklin Gothic Heavy", 25))
        self.label.pack(side="top", pady=20)
        self.label.configure(background="#7cdaf9")
        
    def crear_pestañas(self):
        """
        Crea dos pestañas en la ventana principal de la aplicación y llama a las funciones necesarias para crear los árboles de cada pestaña.

        :return: None
        """
        
        # Creando un objeto Notebook que nos permitirá tener varias pestañas en la ventana.
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(side="top", fill="both", expand=True)

        # Creamos la primera pestaña
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Tabla Inventario")
        self.crear_arbol_inventario()
       
        # Creamos la segunda pestaña
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="Tabla Publico - Historico")
        self.crear_arbol_historico() 
               
    def crear_boton_inicio(self):
        """
        Crea un botón en la ventana para conectarse a la API de Google Drive.

        Returns: None
        """
        # Button que nos permitirá conectar a la API de Google Drive
        # Crear el botón "Iniciar programa"
        self.button = tk.Button(self.root, 
                                text="Iniciar programa", 
                                font=("Arial", 16), 
                                command=self.ejecucion_del_programa)
        self.button.pack(side="top", pady=10)
        self.button.configure(bg="#FFE4C9" )  
    
    def crear_arbol_inventario(self):
        """
        Crea un árbol (TreeView) en la pestaña 1 de la ventana, para mostrar los archivos inventariados.

        Returns: None
        """
        # Crear la tabla
        self.tree = ttk.Treeview(self.tab1)
        self.tree["columns"] = ('file_id','name','extension','owner','visibility','last_modified_date','was_public')
        self.tree.heading("#0", text="id", anchor='center')
        self.tree.heading("file_id", text="file_id", anchor='center')
        self.tree.heading("name", text="name", anchor='center')
        self.tree.heading("extension", text="extension", anchor='center')
        self.tree.heading("owner", text="Owner", anchor='center')
        self.tree.heading("visibility", text="visibility", anchor='center')
        self.tree.heading("last_modified_date", text="last_modified_date", anchor='center')
        self.tree.heading("was_public", text="was_public", anchor='center')
        
        self.tree.column('file_id', width=100)
        self.tree.column('name', width=100)
        self.tree.column('extension', width=80)
        self.tree.column('owner', width=100)
        self.tree.column('visibility', width=100)     
        self.tree.column('last_modified_date', width=120)
        self.tree.column('was_public', width=100)
        
        self.tree.pack(side="bottom", padx=20, pady=10)
    
    def crear_arbol_historico(self):
        """
        Crea un árbol (TreeView) en la pestaña 2 de la ventana, para mostrar el historial de los archivos.

        Returns:  None
        """
        # Crear la tabla
        self.tree = ttk.Treeview(self.tab2)
        self.tree["columns"] = ('file_id','name','extension','owner','last_modified_date')
        self.tree.heading("#0", text="id", anchor='center')
        self.tree.heading("file_id", text="file_id", anchor='center')
        self.tree.heading("name", text="name", anchor='center')
        self.tree.heading("extension", text="extension", anchor='center')
        self.tree.heading("owner", text="Owner", anchor='center')
        self.tree.heading("last_modified_date", text="last_modified_date", anchor='center')
        
        self.tree.column('file_id', width=100)
        self.tree.column('name', width=100)
        self.tree.column('extension', width=80)
        self.tree.column('owner', width=100)
        self.tree.column('last_modified_date', width=120)
        
        self.tree.pack(side="bottom", padx=20, pady=10)
    ########## ALERTAS ##########
    def alerta_google_drive(self):
        """
        Muestra una alerta cuando se conecta correctamente a la API de Google Drive.

        Returns: None
        """
        messagebox.showwarning("Actualizacion", "Conectado a Google Drive con exito.\n Se procede a conectarse con la base de datos") 

    def alerta_base_datos(self):
        """
        Muestra una alerta.

        Args:

        Returns: None.
        
        """
        messagebox.showwarning("Actualizacion","Conectado a la Base de Datos con exito. \n Se procede a listar los archivos en Google Drive")

    def alerta_archivos_listados(self):
        """
        Muestra una alerta con el mensaje.

        Args:

        Returns:  None.
        """
        messagebox.showwarning("Actualizacion","Archivos obtenidos correctamente. \nComienza el análisis.") 
       
    def alerta_finalizacion(self):
        """
        Muestra una alerta con el mensaje. Asimismo, imprime 
        Llama al método completar_tablas_app.

        Args:

        Returns: None.
        """
        
        messagebox.showwarning("Actualizacion","Analisis finalizado. Se hicieron los siguientes cambios: \n - Se pasaron los archivos publicos a privados.")
        print("Se empieza a descargar todo para la aplicacion") 
        self.completar_tablas_app()
    
    def alerta_tablas_completas(self):
        """
        Muestra una alerta y llama al método desconectar_aplicacion.

        Args:

        Returns: None.
        """
        
        messagebox.showwarning("Actualizacion","Analisis finalizado. Se hicieron los siguientes cambios: \n - Se pasaron los archivos publicos a privados.")
        print("Se empieza a descargar todo para la aplicacion") 
        self.desconectar_aplicacion()
        
    ########## FUNCION PARA AGREGAR INFORMACION A LA TABLA ##########
    def add_table_inventario(self, files):
        """
        Agrega cada archivo en la lista de archivos a la tabla de inventario.

        Args:
            files (list): La lista de archivos.

        Returns: None.
        """
        # Obtener la lista de archivos de la API de Google Drive
      
        # Agregar cada archivo como una fila en la tabla
        for file in files:
           # fecha_ultima_modificacion= datetime.datetime.strptime(file['fecha_ultima_modificacion'], '%Y-%m-%dT%H:%M:%S.%fZ')
            self.tree.insert('', 'end', values=(file['id'], 
                                                file['name'], 
                                                file['extension'], 
                                                file['owner'], 
                                                file['visibility'], 
                                                file['fecha_ultima_modificacion'], 
                                                file['was_public']))
             
    def add_table_historico(self, files):
        """
        Agrega cada archivo en la lista de archivos a la tabla histórica.

        Args: files (list): La lista de archivos.

        Returns: None.
        """
        
    # Agregar cada archivo como una fila en la tabla
        for file in files:
            fecha_ultima_modificacion= datetime.datetime.strptime(file['fecha_ultima_modificacion'], '%Y-%m-%dT%H:%M:%S.%fZ')
            self.tree.insert('', 'end', values=(file['id'], 
                                                file['name'], 
                                                file['extension'], 
                                                file['owner'], 
                                                file['fecha_ultima_modificacion']))
    

    ########## RECORRIDO DEL PROGRAMA ##########

    def conectarse_google_drive(self):
        """
        Conecta a la API de Google Drive.

        Args: None
        
        Returns: None
        """
        #Conectar a Google Drive y listar los archivos
        self.driveAPI.connect()
        print("\nConectado a Google Drive - desde Tkinter\n")

    def conectarse_a_SQL(self):
        """
        Opens a connection to a MySQL database, creates and selects a database called "Inventario_Drive".

        Args: None

        Returns: None
        """
        self.db.open_connection()
        #Creo y selecciono una Base de Datos
        self.db.create_database("Inventario_Drive")
        self.db.select_database("Inventario_Drive")

    def crear_tablas_SQL(self):
        """
        Creates two tables in the MySQL database called "Inventario_Drive". 
        The names of the tables are "Inventario_{user}" and "Historico_{user}", where {user} is the name of the authenticated user.

        Args: None

        Returns: None
        """
        
        owner= self.driveAPI.get_authenticated_user()
        owner = owner.split("@")[0]
        nombre_inventario= "Inventario_" + owner
        nombre_inventario_historico= "Historico_" + owner
        
        #Creo las tablas 
        self.db.create_table_inventario(nombre_inventario)
        self.db.create_table_historico(nombre_inventario_historico)

    def list_google_drive_files(self):
        """
        Lists all the files in the Google Drive of the authenticated user and calls the handler_files() function to  inventory the files in the Inventario_Drive database.

        Parameters: None

        Returns: None
        """
        
        flag_fin = self.driveINV.handler_files()
        if flag_fin:
            self.alerta_finalizacion()
        
    ########## FUNCION PARA LOS BOTONES ##########       
    def ejecucion_del_programa(self):
        """
        Main function that executes the program. It connects to the Google Drive of the authenticated user, 
        connects to the Inventario_Drive database, creates tables in the database, lists all the files in the user's Google Drive, 
        and inventories the files in the database.

        Args:  None

        Returns: None
        """
        
        #Conectar a Google Drive y listar los archivos        
        self.conectarse_google_drive()
        self.alerta_google_drive()
        
        #Me conecto a MySQL
        self.conectarse_a_SQL()
        self.crear_tablas_SQL()
        self.alerta_base_datos()

        #Iniciar el inventariado de archivos
        self.list_google_drive_files()

    def completar_tablas_app(self):
        """
        Retrieves the inventory of files in the Inventario_Drive and Historico_{user} tables and adds them to the 
        respective tables in the application's UI. 

        Args:  None

        Returns: None
        """
        
        datos_inv= self.db.pedido_archivos_inventario()
        self.add_table_inventario(datos_inv)
        
        datos_hist= self.db.pedido_archivos_historico()
        self.add_table_inventario(datos_hist)
        
        self.alerta_tablas_completas()
        
    def desconectar_aplicacion(self):
        """
        Closes the connection to the Inventario_Drive database and disconnects the application from the authenticated user's Google Drive.

        Args: None

        Returns: None
        """
        self.db.close_connection()
        self.driveAPI.disconnect()
        
