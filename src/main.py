import tkinter as tk
from google_GUI_Tkinter import App


if __name__ == '__main__':
    
    root = tk.Tk()
    app = App(root) 
    root.mainloop()



"""
if __name__ == '__main__':
    
    datos_env= obtener_variables_env()
    # Carga las variables de entorno desde el archivo .env
    load_dotenv(stream= datos_env)
    # Obtiene las credenciales de la base de datos desde las variables de entorno
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    
    logger = Logger().get_logger()
    driveAPI = GoogleDriveAPI()
    db= Database(db_user, db_password, db_host)
    driveINV = GoogleDriveInventory(db, driveAPI)
    
    app = App(root, logger, driveAPI, db, driveINV) 

    root = tk.Tk()
    root.mainloop()


def obtener_variables_env():
    cipher= Cypher()
    datos_env= cipher.decrypt(flag_cred=0, flag_env=1)
    return io.StringIO(datos_env)
    """