from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


    
#Crea una clase GoogleDriveEmailNotifier para enviar correos electrónicos:
    # Incluye un constructor para configurar las credenciales de acceso al servicio de correo electrónico.
    # Incluye un método send_notification para enviar un correo electrónico al propietario 
    # de un archivo cuando se cambia la configuración de visibilidad de un archivo.
    
#En este ejemplo, la clase GoogleDriveEmailNotifier utiliza la biblioteca smtplib para enviar correos electrónicos mediante el protocolo SMTP. El método send_email acepta los parámetros to (destinatario), subject (asunto), message (cuerpo del mensaje) y attachment (opcionalmente, una ruta de archivo adjunto).

#Dentro del método, se crea un objeto MIMEMultipart que contiene la información del correo electrónico, y se utiliza la biblioteca email.mime para agregar el cuerpo del mensaje y, opcionalmente, el archivo adjunto.

#Luego, se utiliza la función smtplib.SMTP para conectarse al servidor SMTP de Gmail, y se utiliza el método starttls para cifrar la conexión. Luego, se utiliza el método login para autenticarse con la dirección de correo electrónico y la contraseña proporcionadas en el constructor. Finalmente, se utiliza el método sendmail para enviar el correo electrónico al destinatario especificado.
    
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

class GoogleDriveEmailNotifier:
    def __init__(self, email_address, password):
        self.email_address = email_address
        self.password = password

    def send_email(self, to, subject, message, attachment=None):
        msg = MIMEMultipart()
        msg['From'] = self.email_address
        msg['To'] = to
        msg['Subject'] = subject
        body = MIMEText(message)
        msg.attach(body)

        if attachment:
            with open(attachment, 'rb') as f:
                attach = MIMEApplication(f.read(),_subtype='pdf')
                attach.add_header('Content-Disposition','attachment',filename=str(attachment))
                msg.attach(attach)

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email_address, self.password)
            server.sendmail(self.email_address, to, msg.as_string())
            server.quit()
            print("Email sent successfully.")
        except Exception as e:
            print("Error sending email: ", str(e))
    



###################3

# En este ejemplo, la función load_dotenv carga automáticamente las variables de entorno desde el archivo .env en el entorno de ejecución del script. Luego, se pueden acceder a estas variables de entorno utilizando la función os.getenv.

from dotenv import load_dotenv
import os

load_dotenv()

database_host = os.getenv('DATABASE_HOST')
database_user = os.getenv('DATABASE_USER')
database_password = os.getenv('DATABASE_PASSWORD')
database_name = os.getenv('DATABASE_NAME')
gmail_user = os.getenv('GMAIL_USER')
gmail_password = os.getenv('GMAIL_PASSWORD')