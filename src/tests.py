# pip install pytest
import pytest
import os
from dotenv import load_dotenv
from google_Database import Database
from google_DriveAPI import GoogleDriveAPI
from google_Email import EmailNotifier
from logger import Logger

#Ejecutar pytest -v
############################################################################
# ARREGLAR PARA FUTURAS PRUEBAS
############################################################################
@pytest.fixture
def conexion_api():
    """
    Fixture que crea una conexión a la API de Google Drive.

    Args: None

    Returns:
        GoogleDriveAPI: Una instancia de la clase GoogleDriveAPI.
    """
    drive_api = GoogleDriveAPI()
    drive_api.connect()
    file_list = drive_api.test_list_one_file()
    return file_list

@pytest.fixture
def conexion_db():
    """
    Fixture que crea una conexión a la base de datos.

    Args: None

    Returns:
        Database: Una instancia de la clase Database.
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
    return db
############################################################################
############################################################################


# FUNCIONES QUE ACTUALMENTE USO
############################################################################
def listar_archivo_api():
    drive_api = GoogleDriveAPI()
    drive_api.connect()
    file_list = drive_api.test_list_one_file()
    return file_list

def conexion_db():
    """
    Fixture que crea una conexión a la base de datos.

    Args: None

    Returns:
        Database: Una instancia de la clase Database.
    """
    # Carga las variables de entorno desde el archivo .env
    load_dotenv('config/.env')
    # Obtiene las credenciales de la base de datos desde las variables de entorno
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    
    # Pruebo con la Database
    db= Database(db_user, db_password, db_host)
    db.open_connection()
    db.create_database('Test_Drive')
    db.select_database('Test_Drive')
    db.eliminar_table("Test_Inventario") # Si existe la elimino para que quede vacia
    db.create_table_inventario("Test_Inventario")
    
    return db

############################################################################



# Test que se conecta a la API de Google Drive y lista los archivos
def test_connect_drive_and_list_files():
    """
    Test function to check if the Google Drive API is able to connect and list files successfully.

    Args:  None
    Returns: None

    Raises:
        AssertionError: If the length of the list of files returned by the `test_list_one_file` method is not greater than 0.
    """
    file_list= listar_archivo_api()
    conexion_api.disconnect()
    assert len(file_list) > 0

# Test - Guardar los archivos solicitados en la base de datos
def test_save_files_in_database():
    """
    Test que verifica que se puede conectar a Google Drive API, listar los archivos y se guarden en la base de datos
    
    Args: None

    Returns:  None.
    
    Excepciones:
    - AssertionError: si la lista de archivos obtenida está vacía o si ocurre un error al conectar.
    """
    # Conectarse a la API de Google Drive
    file_list= listar_archivo_api()
    db = conexion_db()
     
    for file in file_list:
        db.insertar_archivo_test(file)

    results= db.pedido_archivos_test()
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
    drive_api = GoogleDriveAPI()
    drive_api.connect()
    
    #Es el archivo prueba_pdf.pdf --> Pasar a publico antes de la prueba
    file_id= '19znWgF8kOggXHWnpbZ6ejYUDRYtPaQN8'
    file_visibility_before = drive_api.test_visibility_file(file_id)

    # Cambiar la visibilidad del archivo de público a privado
    drive_api.remove_public_visibility(file_id)
    
    # Verificar que la visibilidad del archivo haya cambiado
    file_visibility_after = drive_api.test_visibility_file(file_id)
    
    assert file_visibility_after == 'privado' and file_visibility_before == "publico"

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



#test_connect_drive_and_list_files()
#logger = Logger().get_logger()
#api= GoogleDriveAPI()
#api.connect()