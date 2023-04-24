import datetime
import os
from googleAPI import GoogleDriveAPI
from googleBD import Database

class GoogleDriveInventory:
    def __init__(self, db):
        #self.drive_api = GoogleDriveAPI(credentials_file_path)
        self.db = Database()
        #self.email = EmailNotifier()
        
    def get_files_list(self):
        #files_list = self.drive_api.get_files()
        #return files_list
        pass
        
    def inventory_files(self, files_list):
        # Imprimo la lista de archivos de la Base de Datos
        bd_list = self.bd.get_files_list()
        
        for file in files_list:
            file_id = file['id']
            file_name = file['name']
            #file_extension = os.path.splitext(file_name)[1]
            file_extension= file['extension']
            #file_owner = file['owners'][0]['emailAddress']
            file_owner = file['owner']
            file_visibility = file['visibility']
            file_modified_time = datetime.datetime.fromisoformat(file['modifiedTime'])
            file_was_public = 1 if file_visibility == 'publico' else 0
 
        
            # Check if the file is already in the inventory
            se_encuentra = self.estaEnInventario(file_name, file_extension)

            if not se_encuentra:
              self.insertar_archivo_nuevo(file_name, file_extension, file_owner, file_visibility, file_modified_time, file_was_public)
              if file_was_public:
                self.insertar_historico(file_name, file_extension, file_owner, file_visibility, file_modified_time)
              
            elif file_visibility == "publico":
              self.handler_visibility(file_id, file_name, file_extension)
    
            else:
              self.chequear_modificacion(file_name, file_extension, file_modified_time)
              
    def estaEnInventario(self, file_name, file_extension):            
      return self.bd.buscar_archivo(file_name, file_extension)
      
    def insertar_archivo_nuevo(self, file_name, file_extension, file_owner, file_visibility, file_modified_time, file_was_public):
      self.db.insertar_archivo(file_name, file_extension, file_owner, file_visibility, file_modified_time, file_was_public)

    def insertar_historico(self, file_name, file_extension, file_owner, file_visibility, file_modified_time):
      self.db.insertar_archivo_historico(file_name, file_extension, file_owner, file_visibility, file_modified_time)

    def chequear_modificacion(self, file_name, file_extension, file_modified_time):

      if self.db.fue_modificado(file_name, file_extension, file_modified_time):
          self.db.update_last_modified_date(file_modified_time)

    def handler_visibility(self, file_id, file_name, file_extension, file_owner):
      last_modified_time = self.cambiar_visibilidad_drive(file_id)
      self.cambiar_visibilidad_bd(file_name, file_extension, last_modified_time)
      self.send_email_owner(file_name, file_extension, file_owner)
    
    def cambiar_visibilidad_drive(self, file_id):
      #self.drive_api.revoke_file_permission(file_id)
      #return time.now()
      pass
    
    def cambiar_visibilidad_bd(self, file_name, file_extension, last_modified_time):
      self.bd.cambiar_visibilidad(file_name, file_extension, last_modified_time)

    def send_email_owner(self, file_name, file_extension, file_owner):
      #subject = f"Change in visibility for file '{file_name}'"
      #body = f"Your file '{file_name}' is no longer publicly visible."
      #self.email.send_email(file_owner, subject, body)
      pass





files_list= [
  {
    "name": "documento1",
    "extension": "pdf",
    "owner": "usuario12@gmail.com",
    "visibility": "publico",
    "fecha_ultima_modificacion": "2022-04-19 13:00:00"
  },
  {
    "name": "imagen1",
    "extension": "png",
    "owner": "usuario2@gmail.com",
    "visibility": "privado",
    "fecha_ultima_modificacion": "2022-04-18 10:30:00"
  },
  {
    "name": "documento",
    "extension": "docx",
    "owner": "usuario3@gmail.com",
    "visibility": "privado",
    "fecha_ultima_modificacion": "2022-04-17 14:45:00"
  }]