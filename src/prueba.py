# Crea una clase GoogleDriveAPI para acceder a la API de Google Drive:
    # Incluye un constructor para configurar las credenciales de acceso a la API de Google Drive.
    # Incluye un método get_files para obtener una lista de archivos de Google Drive del usuario.
    
    

# Crea una clase MySQLConnector para conectarse a la base de datos MySQL:
    #Incluye un constructor para configurar las credenciales de acceso a la base de datos.
    # Incluye métodos para insertar o actualizar registros en la tabla de archivos de Google Drive.
    
    

# Crea una clase GoogleDriveInventory para gestionar el inventario de archivos de Google Drive:    
    #Incluye un constructor para crear instancias de GoogleDriveAPI y MySQLConnector.
    # Incluye métodos para gestionar el inventario de archivos de Google Drive, 
    # como update_file para actualizar un archivo existente en la base de datos, 
    # insert_file para insertar un nuevo archivo en la base de datos y 
    # check_visibility para comprobar y cambiar la configuración de visibilidad de un archivo.


    
#Crea una clase GoogleDriveEmailNotifier para enviar correos electrónicos:
    # Incluye un constructor para configurar las credenciales de acceso al servicio de correo electrónico.
    # Incluye un método send_notification para enviar un correo electrónico al propietario 
    # de un archivo cuando se cambia la configuración de visibilidad de un archivo.
