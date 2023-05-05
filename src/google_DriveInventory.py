import datetime
from google_Email import EmailNotifier
from logger import Logger

class GoogleDriveInventory:
    """ 
    Clase para manejar los archivos de Google Drive.

    """
  ##### FUNCINO DE INICIALIZACION #####
    def __init__(self, db, drive_api):
        """
        Constructor de la clase que inicializa las variables de instancia.
        
        Args:
            db (str): Nombre de la base de datos.
            drive_api (obj): Objeto de la API de Google Drive.
            
        Attributes:
            db (str): Nombre de la base de datos.
            drive_api (obj): Objeto de la API de Google Drive.
            email (obj): Objeto notificador de correo electrónico.
            logger (obj): Objeto logger para la clase.
        
        Returns: None
        """
        self.db = db
        self.drive_api = drive_api
        self.email = EmailNotifier()
        self.logger = Logger().get_logger()
        
    
    ########## FUNCIONES PARA MANEJAR LOS ARCHIVOS ##########
    def handler_files(self):
        """
        Función que maneja los archivos obtenidos de Google Drive. 
        Llama a la función get_files() del objeto DriveAPI para obtener una lista de archivos de Google Drive 
        y los pasa a la función inventory_files() para agregarlos a la tabla de inventario.

        Returns:
          int: 1 si se ejecuta correctamente.
        """
        # obtener una lista de archivos de Google Drive
        files_list =  self.drive_api.get_files()
        # agregar los archivos a la tabla de inventario
        self.inventory_files(files_list)
        
        self.logger.info("Archivos terminados de analizar correctamente")
        print("GoogleDriveInventory: handler_files - inventory_files OUT")
        return 1
    
    def inventory_files(self, files_list):
        """Actualiza la información de los archivos recibidos de Google Drive.

        1) Recorre la lista de archivos recibidos de Google Drive y, para cada archivo, verifica si está registrado en la base de datos. 
        
        2) Si el archivo no está registrado
          - Lo agrega a la base de datos.
          - Si el archivo es público, también se registra en el histórico de archivos públicos y se actualiza su visibilidad.
        
        3) Si el archivo ya está registrado 
          - Verifica si su visibilidad cambio a público
              - Si es publico: Actualiza su información de visibilidad y lo registra en el histórico de archivos públicos.
          
          - Verifica si hubo alguna modificación en la fecha de última modificación. 
            - Si hubo una modificación, actualiza la fecha de última modificación en la base de datos. 
          

        Args:
            files_list (list): Lista de archivos obtenidos de Google Drive.

        Returns:
            int: Retorna 1 una vez que ha completado el proceso de actualización de los archivos.

        """
        
        self.logger.info("Inventory files: Se empiezan a analizar archivo a archivo")
        #Recorro la lista archivo a archivo
        for file in files_list:
            ######## Aca arranca la rutina de comparacion ########
            
            # Me fijo que NO este en la Base de Datos
            if not self.estaEnInventario(file):             
              #Si NO esta  --> Es un Archivo nuevo
              self.handler_archivos_nuevos(file)              
              
            # Si ESTA en la Base de Datos
            else:              
              self.handler_archivos_viejos(file)
            #self.logger.info("Archivo analizado correctamente")
        self.logger.info("Lista de Archivos terminados de analizar correctamente")
        
                
    
     ########## FUNCIONES INSERTAR ARCHIVOS ##########      
    
    def handler_archivos_nuevos(self, file):
      """
        Maneja los archivos nuevos que se encuentran en Google Drive.
        
        Args:
            file (dict): Diccionario con la información del archivo.

        Returns: None
        """
      print("\nSe inserta un archivo en el inventario")
      self.insertar_inventario(file)
      
      if file['visibility'] == "publico":
        # Lo agrego al historico y le cambio la visibilidad
        self.insertar_historico(file)
        self.handler_visibility(file) 

    def handler_archivos_viejos(self, file):
      """
        Maneja los archivos que ya se encuentran en la base de datos.

      Args:
          file (dict): Diccionario con la información del archivo.
      """
      
      if file['visibility'] == 'publico':
        # Si NO esta en el historico lo agrego
        if not self.estaEnHistorico(file):     
          self.insertar_historico(file)
        
        self.handler_visibility(file)
      
      #Chequeo si hubo alguna modificacion en la fecha de ultima modificacion   
      else:
        self.handler_last_modified(file)
        
    
    ######### FUNCIONES AUXILIARES #########
    def estaEnInventario(self, file):     
        """
        Verifica si el archivo recibido de Google Drive está registrado en la base de datos.
        Args:
            file (dict): Diccionario con la información del archivo.

        Returns:
            bool: True si el archivo está registrado en la base de datos, False en caso contrario.
        """
        file_id = file['id']       
        return self.db.existe_archivo(file_id, flag_inventario=1, flag_historico=0)
    
    def estaEnHistorico(self, file): 
      """
        Verifica si el archivo recibido de Google Drive está registrado en la tabla del historico.
        Args:
            file (dict): Diccionario con la información del archivo.

        Returns:
            bool: True si el archivo está registrado en la base de datos, False en caso contrario.
        """           
      return self.db.existe_archivo(file['id'], flag_inventario=0, flag_historico=1)
        
    def insertar_inventario(self, file):
      """
        Inserta un archivo en la base de datos.
        
        Args:
            file (dict): Diccionario con la información del archivo.

        Returns: None
        """
      self.db.insertar_archivo_nuevo(file, flag_inventario=1, flag_historico=0)

    def insertar_historico(self, file):
      """
        Inserta un archivo en la base de datos.
        
        Args:
            file (dict): Diccionario con la información del archivo.

        Returns: None
        """
      self.db.insertar_archivo_nuevo(file, flag_inventario=0, flag_historico=1)

    
    ########## FUNCIONES PARA MANEJAR LA ULTIMA MODIFICACION ##########    
    def handler_last_modified(self, file):
      """
        Actualiza la fecha de última modificación de un archivo en la base de datos en caso de que haya sido modificada.
        
        Args:
            file (dict): Diccionario con la información del archivo.
        Returns: None
        """
      file_id= file['id']
      file_modified_time = datetime.datetime.strptime(file['modified_time'], '%Y-%m-%dT%H:%M:%S.%fZ') 
      
      se_modifico_el_archivo= self.db.fue_modificado(file_id, file_modified_time)
      
      if se_modifico_el_archivo:
        if self.estaEnHistorico(file):
          self.db.update_time(file_id, file_modified_time, flag_inventario=0, flag_historico=1)
        self.db.update_time(file_id, file_modified_time, flag_inventario=1, flag_historico=0)
    
    ########## FUNCIONES PARA CAMBIAR LA VISIBILIDAD ##########   
    def handler_visibility(self, file):
      """
        Actualiza la visibilidad de un archivo en la base de datos en caso de que haya sido modificada.
        
        Args:
            file (dict): Diccionario con la información del archivo.
        Returns: None
        """
      file_id= file['id']
      #Remuevo los permisos publicos
      self.drive_api.remove_public_visibility(file_id)
      
      #Obtengo la ultima hora de la modificacion
      last_modified_time = self.drive_api.get_last_modified_date(file_id)
      last_modified_time = datetime.datetime.strptime(last_modified_time, '%Y-%m-%dT%H:%M:%S.%fZ')
      
      #Update de la Tabla de Inventario --> Aca les paso archivos nuevos
      self.db.update_visibility_inventario(file_id, last_modified_time)
      self.db.update_time(file_id, last_modified_time, flag_inventario=1, flag_historico=0)
      self.db.update_time(file_id, last_modified_time, flag_inventario=0, flag_historico=1)
      #Se envia un mail informando el cambio 
      self.send_email_owner(file)
    
    ########## FUNCIONES PARA MANDAR MAIL ##########    
    def send_email_owner(self, file):
      """
        Envia un mail al dueño del archivo para notificarle que su archivo ya no es publico.        
        Args:
            file(dict): Diccionario con la información del archivo.
        Returns: None
        """   
      #Obtengo el mail del dueño del archivo
      file_owner = file['owner']
      file_name = file['name']
      #Envio el mail
      subject = f"Change in visibility for file '{file_name}'"
      message = f"Your file '{file_name}' is no longer publicly visible."
      self.email.send_email(file_owner, subject, message)
      
      self.logger.info(f"Email sent to inform the change of visibility")
  
      
