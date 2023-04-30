import yagmail

#Crea una clase GoogleDriveEmailNotifier para enviar correos electrónicos:    
class EmailNotifier:
    def __init__(self, email_address, password):
        self.sender = email_address
        self.yag = yagmail.SMTP(self.sender, self.password)

    def send_email(self, recipient, subject, body):
        #self.yag.send(to=recipient, subject=subject, contents=body)
        print("\nSe envio el mail")