import datetime
from google_Email import EmailNotifier
from logger import Logger

class GoogleDriveInventory:
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
    
    ########## FUNCIONES PARA MANEJAR LOS ARCHIVOS ##########
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
        #Recorro la lista archivo a archivo
        for file in files_list:
            file_id = file['id']
            file_modified_time = datetime.datetime.strptime(file['modified_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
            
            #Me fijo si es publico o no
            if file['visibility'] == 'publico':
               file_was_public = 1
            else:
              file_was_public= 0
 
            ######## Aca arranca la rutina de comparacion ########
            
            # Me fijo que NO este en la Base de Datos
            if not self.estaEnInventario(file_id):
              #Si NO esta  --> lo agrego
              self.insertar_archivo(file, file_was_public)

              #Si NO esta y es publico 
              if file_was_public:
                # Lo agrego al historico y le cambio la visibilidad
                self.insertar_historico(file)
                self.handler_visibility(file)                
              
            # Si ESTA en la Base de Datos pero por algun motivo cambiaron el archivo a Publico
            elif file_was_public:
              self.handler_visibility(file, file_id)
            # Si ESTA en la Base de Datos --> Chequear si tuvo alguna modificacion
            else:
              self.handler_last_modified(file_id, file_modified_time)
        
                
    def estaEnInventario(self, file_id):     
      """
        Verifica si el archivo recibido de Google Drive está registrado en la base de datos.
        Args:
            files_id (str): id del archivo

        Returns:
            bool: True si el archivo está registrado en la base de datos, False en caso contrario.
        """       
      return self.db.existe_archivo(file_id)
    
    def estaEnHistorico(self, file_id): 
      """
        Verifica si el archivo recibido de Google Drive está registrado en la tabla del historico.
        Args:
            files_id (str): id del archivo

        Returns:
            bool: True si el archivo está registrado en la base de datos, False en caso contrario.
        """           
      return self.db.existe_archivo_historico(file_id)
      
    ########## FUNCIONES INSERTAR ARCHIVOS ##########      
    def insertar_archivo(self, file, file_was_public):
      """
        Inserta un archivo en la base de datos.
        
        Args:
            file (dict): Diccionario con la información del archivo.
            file_was_public (bool): True si el archivo es público, False en caso contrario.

        Returns: None
        """
      self.db.insertar_archivo_nuevo(file, file_was_public)

    def insertar_historico(self, file):
      """
        Inserta un archivo en la base de datos.
        
        Args:
            file (dict): Diccionario con la información del archivo.

        Returns: None
        """
      self.db.insertar_archivo_historico(file)

    
    ########## FUNCIONES PARA MANEJAR LA ULTIMA MODIFICACION ##########    
    def handler_last_modified(self, file_id, file_modified_time):
      """
        Actualiza la fecha de última modificación de un archivo en la base de datos en caso de que haya sido modificada.
        
        Args:
            file_id(str): id del archivo.
            file_modified_time (datetime): Fecha de última modificación del archivo.

        Returns: None
        """
      if self.db.fue_modificado(file_id, file_modified_time):
          self.db.update_last_modified_date(file_id, file_modified_time)

    
    ########## FUNCIONES PARA CAMBIAR LA VISIBILIDAD ##########   
    def handler_visibility(self, file,  file_id):
      """
        Actualiza la visibilidad de un archivo en la base de datos en caso de que haya sido modificada.
        
        Args:
            file(dict): Diccionario con la información del archivo.
            file_id(str): id del archivo.
        Returns: None
        """      
      #Remuevo los permisos publicos
      self.drive_api.remove_public_visibility(file_id)
      
      #Obtengo la ultima hora de la modificacion
      last_modified_time = self.drive_api.get_last_modified_date(file_id)
      
      last_modified_time = datetime.datetime.strptime(last_modified_time, '%Y-%m-%dT%H:%M:%S.%fZ')
      
      #Update de la Tabla de Inventario
      self.db.update_handler_visibility(file_id, last_modified_time)
      
      # Si ya estaba le actualizo la ultima modificacion
      if self.estaEnHistorico(file_id): 
        self.db.update_archivo_historico(file_id, last_modified_time)
      else:
        self.db.insertar_archivo_historico(file)
        
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
  
      
