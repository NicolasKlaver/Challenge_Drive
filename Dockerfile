# Usar la imagen oficial de Python 3.9 como base
FROM python:3.9

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Copiar el archivo requirements.txt a la imagen
COPY requirements.txt .

# Instalar las dependencias
#RUN pip install -r requirements.txt
RUN pip install mysql-connector google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client yagmail pytest


# Copiar el código fuente de la aplicación a la imagen
COPY src/ .
#COPY src/ ./src
COPY config/ .
COPY tests/ .
COPY Logs/ .

# Exponer el puerto 5000
EXPOSE 5000

# Iniciar la aplicación
CMD ["python", "src/main.py"]








##############################################################
##############################################################
#  Crear imagen
#docker build -t nombre_de_la_imagen .

# Ejecutar contenedor
#docker run -p 5000:5000 nombre_de_la_imagen
##############################################################
##############################################################
