from cryptography.fernet import Fernet
import json

class Cypher:
    def __init__(self):
        """
        Constructor de la clase Cypher.
        Cargo las rutas a los archivos y la clave
        """
        self.ruta_credential = 'config/credential_drive.json'
        self.ruta_env = 'config/.env'

        #self.ruta_clave= 'config/clave.key'
        self.key="PnUsoKJUeQn8xoZtCfRGc9aibuzq7XnFuT5t-ePbwuM="
        self.ruta_cifrado_cred= "config/credential_drive.json.encrypted"
        self.ruta_cifrado_env= "config/.env.encrypted"
    
    def encrypt(self):  
        """
        Funcion que cifra un archivo
        """
        #Abro el archivo y lo guardo en una variable archivo_original
        with open(self.ruta_credential, 'rb') as archivo_original:
            datos_credential = archivo_original.read() 
            
        with open(self.ruta_env, 'rb') as archivo_original:
            datos_env = archivo_original.read()     

        #Creo un objeto Fernet con la clave generada
        clave = Fernet.generate_key()
        fernet = Fernet(clave)
        # Encripto los datos
        datos_cifrados_credencial = fernet.encrypt(datos_credential) 
        datos_cifrados_env = fernet.encrypt(datos_env) 
        
        # Abre el archivo cifrado y lo guarda
        with open(self.ruta_credential + '.encrypted', 'wb') as archivo_cifrado:
            archivo_cifrado.write(datos_cifrados_credencial)
            
        with open(self.ruta_env + '.encrypted', 'wb') as archivo_cifrado:
            archivo_cifrado.write(datos_cifrados_env)
        
        # Guardar la clave en un archivo
        # Abre un nuevo archivo llamado clave.key en modo escritura binaria ('wb') y lo guarda en una variable llamada archivo_clave
        with open(self.ruta_clave, 'wb') as archivo_clave:
            archivo_clave.write(clave)
    
    def decrypt(self, flag_cred, flag_env):
        """
        Funcion que desencripta un archivo

        Returns:
            datos(bytes): datos desencriptados del archivo
        """
        # Cargar la clave desde el archivo
        #with open(self.ruta_clave, 'rb') as archivo_clave:
        #    clave = archivo_clave.read()

        # Desencriptar el archivo 
        if flag_cred:
            with open(self.ruta_cifrado_cred, 'rb') as archivo_cifrado:
                datos_cifrados = archivo_cifrado.read()
        elif flag_env:
            with open(self.ruta_cifrado_env, 'rb') as archivo_cifrado:
                datos_cifrados = archivo_cifrado.read()

        fernet = Fernet(self.key)
        datos = fernet.decrypt(datos_cifrados)
        # Convertir el contenido desencriptado en una cadena de texto
        decrypted_text = datos.decode()
        # Eliminar los caracteres adicionales del texto desencriptado
        decrypted_text = decrypted_text.strip()
        
        if flag_cred:
            decrypted_text = json.loads(decrypted_text)
        
        return decrypted_text
    
    
    
#cipher = Cypher()
#cipher.encrypt()

#datos= cipher.decrypt(flag_cred=0,flag_env=1)
#print(datos)
# Convertir el contenido desencriptado en una cadena de texto
#decrypted_text = datos.decode()
# Eliminar los caracteres adicionales del texto desencriptado
#decrypted_text = decrypted_text.strip()

#print("\n\nArchivo cifrado:\n ", datos)

