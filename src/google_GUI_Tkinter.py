import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from google_DriveAPI import GoogleDriveAPI
from google_Database import Database
from google_DriveInventory import GoogleDriveInventory
from dotenv import load_dotenv
import os
from logger import Logger

class App:
    """
    Clase que representa la interfaz de usuario de la aplicación.
    """
    def __init__(self, root):
        """
        Inicializa la interfaz de usuario y todas las variables necesarias para conectarse con la base de datos y con la API de Google Drive.

        Args:
            root: Objeto Tk que representa la ventana principal de la aplicación.
        
        Returns: None
        """
        
        
        
        # Carga las variables de entorno desde el archivo .env
        load_dotenv('config/.env')
        # Obtiene las credenciales de la base de datos desde las variables de entorno
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")
        
        self.logger = Logger().get_logger()
        self.driveAPI = GoogleDriveAPI()
        self.db= Database(db_user, db_password, db_host)
        self.driveINV = GoogleDriveInventory(self.db, self.driveAPI)
        
        self.db.logger= self.logger
        self.driveINV.logger= self.logger
        #self.driveAPI.logger=self.logger

        
        # Definimos el objeto raíz de la aplicación y estableciendo el título de la ventana.
        self.root = root
        self.root.title("Challenge Docs en Drive Publico")
        self.root.configure(background="#7cdaf9")
        
        # self.root.protocol("WM_DELETE_WINDOW", self.salirAplicacion())
        
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
        self.tree_inv = ttk.Treeview(self.tab1)
        self.tree_inv["columns"] = ('id','file_id','name','extension','owner','visibility','last_modified_date')
        self.tree_inv.heading("#0", text="", anchor='center')
        self.tree_inv.heading("id", text="id", anchor='center')
        self.tree_inv.heading("file_id", text="file_id", anchor='center')
        self.tree_inv.heading("name", text="name", anchor='center')
        self.tree_inv.heading("extension", text="extension", anchor='center')
        self.tree_inv.heading("owner", text="Owner", anchor='center')
        self.tree_inv.heading("visibility", text="visibility", anchor='center')
        self.tree_inv.heading("last_modified_date", text="last_modified_date", anchor='center')
        
        self.tree_inv.column("#0", width=0)
        self.tree_inv.column("id", width=60)
        self.tree_inv.column('file_id', width=200)
        self.tree_inv.column('name', width=200)
        self.tree_inv.column('extension', width=100)
        self.tree_inv.column('owner', width=200)
        self.tree_inv.column('visibility', width=100)     
        self.tree_inv.column('last_modified_date', width=200)
        
        self.tree_inv.pack(side="bottom", padx=20, pady=10)
    
    def crear_arbol_historico(self):
        """
        Crea un árbol (TreeView) en la pestaña 2 de la ventana, para mostrar el historial de los archivos.

        Returns:  None
        """
        # Crear la tabla
        self.tree_hist = ttk.Treeview(self.tab2)
        self.tree_hist["columns"] = ('id','file_id','name','extension','owner','last_modified_date')
        self.tree_hist.heading("id", text="id", anchor='center')
        self.tree_hist.heading("file_id", text="file_id", anchor='center')
        self.tree_hist.heading("name", text="name", anchor='center')
        self.tree_hist.heading("extension", text="extension", anchor='center')
        self.tree_hist.heading("owner", text="Owner", anchor='center')
        self.tree_hist.heading("last_modified_date", text="last_modified_date", anchor='center')
        
        self.tree_hist.column('id', width=20)
        self.tree_hist.column('file_id', width=200)
        self.tree_hist.column('name', width=100)
        self.tree_hist.column('extension', width=80)
        self.tree_hist.column('owner', width=150)
        self.tree_hist.column('last_modified_date', width=120)
        
        self.tree_hist.pack(side="bottom", padx=20, pady=10)
    
    
    ########## ALERTAS ##########
    def alerta_google_drive(self):
        """
        Muestra una alerta cuando se conecta correctamente a la API de Google Drive.

        Returns: None
        """
        #messagebox.showwarning("Actualizacion", "Conectado a Google Drive con exito.\n Se procede a conectarse con la base de datos") 
        messagebox.showinfo("Conexion Exitosa", "Conectado a Google Drive con exito.\n Se procede a conectarse con la base de datos")
        #self.root.mainloop()
           
    def alerta_base_datos(self):
        """
        Muestra una alerta.

        Args:

        Returns: None.
        
        """
        messagebox.showinfo("Conexion exitosa","Conectado a la Base de Datos y creadas las tablas con exito. \n Se procede a listar los archivos en Google Drive")
       # messagebox.showwarning("Actualizacion","Conectado a la Base de Datos con exito. \n Se procede a listar los archivos en Google Drive")

    def alerta_archivos_listados(self):
        """
        Muestra una alerta con el mensaje.

        Args:

        Returns:  None.
        """
        messagebox.showinfo("Archivos obtenidos","Archivos obtenidos con exito. \nComienza el análisis.")
        #messagebox.showwarning("Actualizacion","Archivos obtenidos correctamente. \nComienza el análisis.") 
       
    def alerta_finalizacion(self):
        """
        Muestra una alerta con el mensaje. Asimismo, imprime 
        Llama al método completar_tablas_app.

        Args:

        Returns: None.
        """
        messagebox.showinfo("Completado con exito","Analisis finalizado: \n Se agregaron archivos a la Base de Datos \n - Se pasaron los archivos publicos a privados.")
       # messagebox.showwarning("Actualizacion","Analisis finalizado. Se hicieron los siguientes cambios: \n - Se pasaron los archivos publicos a privados.")
        
        print("Se empieza a descargar todo para la aplicacion") 
        self.completar_tablas_app()
    
    def alerta_tablas_completas(self):
        """
        Muestra una alerta y llama al método desconectar_aplicacion.

        Args:

        Returns: None.
        """
        
        messagebox.showwarning("Programa Finalizado","Se termino el programa. \n Se desconecta de la base de datos y de Google Drive.")
        print("Se empieza a descargar todo para la aplicacion") 
        self.desconectar_aplicacion()
        #self.salirAplicacion()
        
    def salirAplicacion(self):
        valor = messagebox.askquestion("Salir", "¿Está seguro que desea salir de la Aplicación?")
        if valor == "yes":
            self.root.destroy()  
  
    ########## FUNCION PARA AGREGAR INFORMACION A LA TABLA ##########
    def add_table_inventario(self, files):
        """
        Agrega cada archivo en la lista de archivos a la tabla de inventario.

        Args:
            files (list): La lista de archivos.

        Returns: None.
        """
        # Seleccionar la primera pestaña
        self.notebook.select(self.tab1)
        
        # Obtener la tabla de la primera pestaña
        #table = self.tabla1
      
        # Agregar cada archivo como una fila en la tabla
        for file in files:
            print("Imprimo un archivo que se esta agregando: ", file)
           # fecha_ultima_modificacion= datetime.datetime.strptime(file['fecha_ultima_modificacion'], '%Y-%m-%dT%H:%M:%S.%fZ')
            self.tree_inv.insert('', 'end', values=(file['id'],
                                                file['file_id'], 
                                                file['name'], 
                                                file['extension'], 
                                                file['owner'], 
                                                file['visibility'], 
                                                file['fecha_ultima_modificacion']))
             
    def add_table_historico(self, files):
        """
        Agrega cada archivo en la lista de archivos a la tabla histórica.

        Args: files (list): La lista de archivos.

        Returns: None.
        """
        # Seleccionar la primera pestaña
        self.notebook.select(self.tab2)
        
       
    # Agregar cada archivo como una fila en la tabla
        for file in files:
           # fecha_ultima_modificacion= datetime.datetime.strptime(file['fecha_ultima_modificacion'], '%Y-%m-%dT%H:%M:%S.%fZ')
            self.tree_hist.insert('', 'end', values=(file['id'],
                                                file['file_id'], 
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
        
        datos_inv= self.db.pedido_archivos(flag_inventario=1, flag_historico=0)
        self.add_table_inventario(datos_inv)
        
        datos_hist= self.db.pedido_archivos(flag_inventario=0, flag_historico=1)
        self.add_table_historico(datos_hist)
        
        self.alerta_tablas_completas()
        
    def desconectar_aplicacion(self):
        """
        Closes the connection to the Inventario_Drive database and disconnects the application from the authenticated user's Google Drive.

        Args: None

        Returns: None
        """
        self.db.close_connection()
        self.driveAPI.disconnect()
        
