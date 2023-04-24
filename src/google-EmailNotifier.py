import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


#Crea una clase GoogleDriveEmailNotifier para enviar correos electrónicos:
class EmailNotifier:
    # Incluye un constructor para configurar las credenciales de acceso al servicio de correo electrónico.
    def __init__(self, email_address, password):
        self.email_address = email_address
        self.password = password
    
    # Incluye un método send_notification para enviar un correo electrónico al propietario 
    def send_email(self, file_owner, subject, message):
        
        # Se crea un objeto MIMEMultipart que contiene la información 
        # y se utiliza la biblioteca email.mime para agregar el cuerpo del mensaje
        msg = MIMEMultipart()
        msg['From'] = self.email_address
        msg['To'] = file_owner
        msg['Subject'] = subject
        
        body = MIMEText(message)
        msg.attach(body)
        
        try:
            #Se utiliza la función smtplib.SMTP para conectarse al servidor SMTP de Gmail, 
            server = smtplib.SMTP('smtp.gmail.com', 587)
            # Se utiliza el método starttls para cifrar la conexión.
            server.starttls()
            # se utiliza el método login para autenticarse con la dirección de correo electrónico y la contraseña
            # proporcionadas en el constructor. 
            server.login(self.email_address, self.password)
            #Se envia el mail
            server.sendmail(self.email_address, file_owner, msg.as_string())
            server.quit()
            print("Email sent successfully.")
        except Exception as e:
            print("Error sending email: ", str(e))
    

nuevo_email= EmailNotifier("nicooklaver@gmail.com", "nicolas98")
nuevo_email.send_email("testdepython1009@gmail.com", "test", "test")

