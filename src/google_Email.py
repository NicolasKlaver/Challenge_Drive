import yagmail
from dotenv import load_dotenv
import os
from logger import Logger

#Crea una clase GoogleDriveEmailNotifier para enviar correos electrónicos:    
class EmailNotifier:
    def __init__(self):
        """
        Inicializa la clase EmailManager.

        Carga las variables de entorno desde el archivo .env y obtiene las credenciales de la base de datos desde las variables de entorno. 
        También crea una instancia de  Yagmail.SMTP para el envío de correos electrónicos y una instancia de Logger para el registro de eventos.

        Args: 
            None

        Returns:
            None
        """
        # Carga las variables de entorno desde el archivo .env
        load_dotenv('config/.env')
        # Obtiene las credenciales de la base de datos desde las variables de entorno
        em_user = os.getenv("EM_USER")
        em_password = os.getenv("EM_PASSWORD")
        self.yag = yagmail.SMTP(em_user, em_password)
        self.logger = Logger().get_logger()
        
    def send_email(self, recipient, subject, body):
        """
        Envía un correo electrónico a un destinatario con un asunto y un cuerpo.
        
        Args:
            recipient (str): Correo electrónico del destinatario.
            subject (str): Asunto del correo electrónico.
            body (str): Cuerpo del correo electrónico.

        Returns: None

        Raises:
            yagmail.YagAddressError: Si el correo electrónico del destinatario no es válido.
            yagmail.YagConnectionClosed: Si no se puede establecer conexión con el servidor SMTP.
        """
        try: 
            self.yag.send(to=recipient, subject=subject, contents=body)
            self.logger.info("Correo electrónico enviado correctamente.")
            print("\nSe envio el mail")
            
        except (yagmail.YagAddressError, yagmail.YagConnectionClosed) as e:
            self.logger.error(f"Error al enviar correo electrónico: {e}")
            raise e
            
            
            