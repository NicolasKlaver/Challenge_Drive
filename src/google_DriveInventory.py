import datetime
import os
from google_DriveAPI import GoogleDriveAPI
from google_Database import Database

class GoogleDriveInventory:
    def __init__(self, db, drive_api):
        self.drive_api = drive_api
        self.db = db
        #self.emailObject = EmailNotifier()
        
    def get_files_list(self):
        return self.drive_api.get_files()
        
    def inventory_files(self, files_list):
        # Imprimo la lista de archivos de la Base de Datos
        #bd_list = self.bd.get_files_list()
        print("\n\nG-INV: files_list: " )
        for file in files_list:
            file_id = file['id']
            print("File id: ",  file_id)
            file_name = file['name']
            print("name: ",  file_name)
            #file_extension = os.path.splitext(file_name)[1]
            file_extension= file['extension']
            print("Extension id: ",  file_extension)
            #file_owner = file['owners'][0]['emailAddress']
            file_owner = file['owner']
            file_visibility = file['visibility']
            file_modified_time = datetime.datetime.strptime(file['modified_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
            #file_modified_time = datetime.datetime.fromisoformat(file['modified_time'])
            file_was_public = 1 if file_visibility == 'publico' else 0
 
        
            # Check if the file is already in the inventory
            se_encuentra = self.estaEnInventario(file_name, file_extension)

            if not se_encuentra:
              self.insertar_archivo(file_name, file_extension, file_owner, file_visibility, file_modified_time, file_was_public)
               
              if file_was_public:
                self.insertar_historico(file_name, file_extension, file_owner, file_visibility, file_modified_time)
              
            elif file_visibility == "publico":
              self.handler_visibility(file_id, file_name, file_extension)
    
            else:
              self.handler_last_modified(file_name, file_extension, file_modified_time)
              
    
    def estaEnInventario(self, file_name, file_extension):            
      return self.db.buscar_archivo(file_name, file_extension)
      
    def insertar_archivo(self, file_name, file_extension, file_owner, file_visibility, file_modified_time, file_was_public):
      self.db.insertar_archivo_nuevo(file_name, file_extension, file_owner, file_visibility, file_modified_time, file_was_public)

    def insertar_historico(self, file_name, file_extension, file_owner, file_visibility, file_modified_time):
      self.db.insertar_archivo_historico(file_name, file_extension, file_owner, file_visibility, file_modified_time)

    def handler_last_modified(self, file_name, file_extension, file_modified_time):

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
      subject = f"Change in visibility for file '{file_name}.{file_extension}'"
      message = f"Your file '{file_name}' is no longer publicly visible."
      self.emailObject.send_email(file_owner, subject, message)
      



