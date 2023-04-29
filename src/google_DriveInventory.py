import datetime

class GoogleDriveInventory:
  ##### FUNCINO DE INICIALIZACION #####
    def __init__(self, db, drive_api):
        #self.obj_app = App()
        self.db = db
        self.drive_api = drive_api
        #self.emailObject = EmailNotifier()
        
    
    def handler_files(self):
        files_list =  self.drive_api.get_files()
        #self.obj_app .alerta_archivos_listados()
        self.inventory_files(files_list)
        print("GoogleDriveInventory: handler_files - inventory_files OUT")
        return 1
    
    ########## FUNCIONES PARA MANEJAR LOS ARCHIVOS ##########
    def inventory_files(self, files_list):
        for file in files_list:
            file_id = file['id']
            file_modified_time = datetime.datetime.strptime(file['modified_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
                       
            if file['visibility'] == 'publico':
               file_was_public = 1
            else:
              file_was_public= 0
 
            ######## Aca arranca la rutina de comparacion ########
            
            # Me fijo que NO este en la Base de Datos
      
            if not self.estaEnInventario(file_id):
              self.insertar_archivo(file, file_was_public)

              #Si NO esta  --> lo agrego
              if file_was_public:
                #LLega hasta aca
                self.insertar_historico(file)
                self.handler_visibility(file)                
              
            # Si ESTA en la Base de Datos pero por algun motivo cambiaron el archivo a Publico
            elif file_was_public:
              self.handler_visibility(file, file_id)
            # Si ESTA en la Base de Datos --> Chequear si tuvo alguna modificacion
            else:
              self.handler_last_modified(file_id, file_modified_time)
        
        #self.obj_app.alerta_finalizacion()
                
    def estaEnInventario(self, file_id):            
      return self.db.existe_archivo(file_id)
    
    def estaEnHistorico(self, file_id):            
      return self.db.existe_archivo_historico(file_id)
      
    ########## FUNCIONES INSERTAR ARCHIVOS ##########      
    def insertar_archivo(self, file, file_was_public):
      self.db.insertar_archivo_nuevo(file, file_was_public)

    def insertar_historico(self, file):
      self.db.insertar_archivo_historico(file)

    
    ########## FUNCIONES PARA MANEJAR LA ULTIMA MODIFICACION ##########    
    def handler_last_modified(self, file_id, file_modified_time):
      if self.db.fue_modificado(file_id, file_modified_time):
          self.db.update_last_modified_date(file_id, file_modified_time)

    
    ########## FUNCIONES PARA CAMBIAR LA VISIBILIDAD ##########   
    def handler_visibility(self, file,  file_id):
      file_owner = file['owner']
      print("\n\nFile ownwer: ", file_owner)
      
      #Remuevo los permisos publicos
      self.drive_api.remove_public_visibility(file_id)
      
      #Obtengo la ultima hora de la modificacion
      last_modified_time = self.drive_api.get_last_modified_date(file_id)
      print("\nLast_mofiied_time", last_modified_time)
      last_modified_time = datetime.datetime.strptime(file['modified_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
      print("\nLast_mofiied_time", last_modified_time)
      #Update de la Tabla de Inventario
      self.db.update_handler_visibility(file_id, last_modified_time)
      
      # Si ya estaba le actualizo la ultima modificacion
      if self.estaEnHistorico(file_id): 
        self.db.update_archivo_historico(file_id, last_modified_time)
      else:
        self.db.insertar_archivo_historico(file)
        
      self.send_email_owner(file_id, file_owner)
    
  
    ########## FUNCIONES PARA MANDAR MAIL ##########    
    def send_email_owner(self, file_name, file_extension, file_owner):
      #subject = f"Change in visibility for file '{file_name}.{file_extension}'"
      #message = f"Your file '{file_name}' is no longer publicly visible."
      #self.emailObject.send_email(file_owner, subject, message)
      pass
      
