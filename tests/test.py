# pip install pytest
import pytest
import os
from dotenv import load_dotenv
from google_Database import Database
from google_DriveAPI import GoogleDriveAPI
from google_Email import EmailNotifier



# Test que se conecta a la API de Google Drive y lista los archivos
def test_connect_drive_and_list_files():
    """
    Test function to check if the Google Drive API is able to connect and list files successfully.

    Args:  None
    Returns: None

    Raises:
        AssertionError: If the length of the list of files returned by the `test_list_one_file` method is not greater than 0.
    """
    
    drive_api = GoogleDriveAPI()
    drive_api.connect()
    file_list = drive_api.test_list_one_file()
    assert len(file_list) > 0

# Test - Guardar los archivos solicitados en la base de datos
def test_save_files_in_database():
    """
    Test que verifica que se puede conectar a Google Drive API y listar los archivos.
    
    Args: None

    Returns:  None.
    
    Excepciones:
    - AssertionError: si la lista de archivos obtenida está vacía o si ocurre un error al conectar.
    """
    
    # Carga las variables de entorno desde el archivo .env
    load_dotenv('config/.env')
    # Obtiene las credenciales de la base de datos desde las variables de entorno
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    
    # Pruebo con la Da
    db= Database(db_user, db_password, db_host)
    db.open_connection()
    db.create_database('Test_Drive')
    db.select_database('Test_Drive')
    db.create_table_inventario("Test_Inventario")

    # Conectarse a la API de Google Drive
    drive_api.connect()
    file = drive_api.test_list_one_file()
    
    #Me fijo si es publico o no
    if file['visibility'] == 'publico':
        file_was_public = 1
    else:
        file_was_public= 0
     
    db.insertar_archivo_nuevo(file, file_was_public)
    drive_api.disconnect()
    
    results= db.pedido_archivos_inventario()
    db.close_connection()
    assert len(results) > 0
    
    
# Cambiar la visibilidad del archivo de público a privado
def test_change_visibility():
    """
    Test que verifica que se puede cambiar la visibilidad de un archivo en Google Drive API.
    
    Parámetros: None

    Salida: None.
    
    Excepciones:
    - AssertionError: si la visibilidad del archivo no cambia correctamente o si ocurre un error al conectar.
    """
    # Conectarse a la API de Google Drive
    drive_api= GoogleDriveAPI()
    drive_api.connect()
    
    file_id= "asd"
    file_visibility = drive_api.visibility_file(file_id)
    print("Verificar la visibilidad del file_id: ", file_visibility)
    
    # Cambiar la visibilidad del archivo de público a privado
    drive_api.remove_public_visibility(file_id)
    
    # Verificar que la visibilidad del archivo haya cambiado
    file_visibility = drive_api.list_files(file_id)
    
    assert file_visibility == 'privado'


# Enviar un correo electrónico al Propietario del archivo, avisando que la visibilidad ha sido cambiada
def test_email():
    """
    Test que verifica que se puede enviar un correo electrónico usando la clase EmailNotifier.
    
    Args: None

    Return: None.
    
    Excepciones:
    - AssertionError: si ocurre un error al enviar el correo electrónico.
    """
    email= EmailNotifier()
    recipient= "nicooklaver@gmail.com"
    subject= "Prueba de correo electrónico"
    body="Esto es una prueba de correo electrónico"
    
    assert email.send_email(recipient, subject, body) == None
    