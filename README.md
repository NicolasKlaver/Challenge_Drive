# Challenge Docs en Drive Públicos
- Desarrollar una aplicación para inventariar en una Base de Datos todos los archivos pertenecientes a la unidad de Drive de un usuario.

![](https://github.com/NicolasKlaver/Challenge_Drive/blob/main/img/programa.jpg)


# Ejecucion del programa
1)  Debera tener instaladas las bibliotecas necesarias
- pip install pytest yagmail google-auth-httplib2 google-auth-oauthlib google-api-python-client python-dotenv mysql-connector-python cryptography
  - Tener instalado y ejecutandose el servicio de MySQL.
  - git clone https://github.com/NicolasKlaver/Challenge_Drive.git
  - Ejecutar el archivo "main.py" (desde el directorio de trabajo)

2) Abrir Docker Desktop
- Es necesario ejecutar el programa de la forma anterior, para tener el token de acceso a su cuenta (no encontre la forma de entrar a su cuenta de Google Drive ejecutando desde Docker)
- For Windows:[ Instalar Xming X Server](ruta)
- Ir a la ubicacion donde se descargo y en una terminar ejecutar el comando: "Xming.exe -ac"
- En el archivo Dockerfile_python, debera cambiar en DISPLAY=SU_DIRECCION-IP:0.0
- En el directorio del proyecto ejecutar: docker-compose up

#### Instalar bibliotecas para ejecutar:
- pip install pytest yagmail google-auth-httplib2 google-auth-oauthlib google-api-python-client python-dotenv mysql-connector-python cryptography


# Aclaraciones acerca de la construccion y el objetivo del programa.
 - Realice el programa pensando que trabajo en el área de Seguridad Informática, y que el objetivo es tratar con archivos sensibles que pueden llegar a ser publicos. 
 - Por eso, como podras ver mas adelante, el usuario no tiene relación ni elección con la ejecución del programa, si no que se le deberá explicar de que se trata y ejecutarlo en caso de que este de acuerdo.
- Por un tema practico de no tener que compartir archivos, estoy usando la clave para desencriptar las credenciales y contraseñas como un string.
- Mi objetivo con el tratamiento de las credenciales es que cada cierto tiempo a determinar automatizar un script para que genere nuevas key y se actualice en la carpeta del usuario donde lo tenga instalado.



## Estructuras de las carpetas
- Challenge_Meli:
    - src:
      - google_Database: contiene en la clase "Database" toda la lógica relacionada con la Base de Datos.
      - google_DriveAPI: contiene en la clase "GoogleDriveAPI" toda la logica relacionado con la API de google drive.
      - google_DriveInventory: contiene en la clase "GoogleDriveInventory" la lógica para analizar y manipular los archivos obtenidos de google drive.
      - google_Email: contiene en la clase "EmailNotifier" la logica para enviar correos electronicos.
      - google_GUI_Tkinter: contiene la clase "App" donde se encuentra la parte de la Interfaz Grafica y la lógica para ejecutar el programa.
      - logger: contiene la clase "Logger" que se utiliza para imprimir los logs correspondientes.
      - main: contiene la ejecucion del programa.
      - cifrado: contiene la clase para encriptar y desencriptar archivos.
    
    - Logs:
      - log_info: contiene los logs de la ejecucion.
    
    - Tests:
      - test_general: contienen los tests para probar el programa.
  
    - Config:
      - credential_drive.json.encrypted: credenciales para google drive
      - .env.encrypted: archivo con las variables y contraseñas.
      - requirement.txt: archivo que le paso a docker con las librerias necesarias para ejecutar el programa.
      - clave.key: contiene la clave para desencriptar los archivos
    
    - Dockerfile_python: configuracion de la imagen de python.
    - Dockerfile_mysql: configuracion de la imagen de mysql.
    - Dockerfile-compose.yml: conexion de estas dos imagenes.


# Puntos Pendientes
- Mejorar los tests, faltan crear modelos para generar mas pruebas y organizarlos mejor.
-  Separar en una nueva clase la Interfaz grafica de la ejecucion del programa.
-  Para la ejecucion del programa pensaba crear una maquina de estado.
- Mejorar la interfaz grafica para que tenga mas informacion y seguridad.


  # Explicacion de la estructura del codigo

1) El archivo "google_GUI_Tkinter.py" ejecuta la interfaz gráfica y una vez el usuario haga click en el boton "Iniciar Programa" saldrá un mensaje de alerta el cual deberá aceptar.

   
2) Una vez aceptado, se lanza un pedido para conectarse a Google Drive, en caso de que sea exitoso, se crea una Base de Datos(* 1  *) y se selecciona para poder trabajar con ella.
   Una vez conectado, se crean dos tablas: una para el Inventario en general, y otra para el historico (2). Se utiliza el nombre del owner de la cuenta que lo obtenemos haciendole un pedido a GoogleDriveAPI.



(1) En este caso creo una base de datos general para todos los usuarios y multiples tablas por cada uno, pero es un requirimiento que facilmente puede cambiar por eso llamo a la funcion "create_database" aunque solo la utilice una vez. (1)

(2) Para este caso no considero que sea necesaria tener dos tablas, ya que la tabla inventario contiene un parámetro que informa si un archivo fue público. Pero considerando que en un futuro se pueda sumar lógica para sacar de la tabla archivos eliminados, en este caso utilizo una tabla como back-up para no perder la información de los archivos que alguna vez fueron públicos. (2)



3) La ejecución sigue en el archivo "google_DriveInventory.py" donde hago un pedido a la clase de Google Drive para listar los archivos con el metodo "handler_files". 



4) Una vez obtenidos con exito, analizo en un for un archivo a la vez con el metodo "inventory_files". Lo primero que hago es ver si se encuentran en el Inventario.
  
  4.1) Analisis con archivos que NO estan en el Inventario, metodo "handler_archivos_nuevos".
    
  - Inserto el archivo en la Database.
    
  - Si ademas, el archivo es publico:
     
   -  Lo cargo en el Historico.
     
   -  "handler_visibility": Lanzo una solicitud a GoogleDriveAPI para cambiar la Visibilidad. Una vez hecho este cambio, hago una consulta para obtener la hora de la ultima modificación hecha y actualizo la visibilidad a la tabla Inventario y la hora de modificacion a ambas tablas(*3*).
   
   - Finalmente mando un email al usuario indicando el cambio.



(3) Esta logica creo que se puede mejorar o cambiar, sobre todo si le diera mas libertad al usuario para ver sus cosas. 
En esta caso estoy cargando un archivo nuevo con Visibilidad publica y en el mismo transcurso del programa lo actualizo a privado. (*3*)  



  4.2) Archivos que estan en el inventario, metodo "handler_archivos_viejos".
    
   - Si el archivo es publico, lo cargo en el histórico en caso de que no este y llamo como arriba al metodo handler_visibility.
    
   - Si no es publico, chequeo si fue modificado lanzando una consulta a la Database y comparando la hora con la actual, con el metodo "handler_last_modified". En caso que que corresponda se actualizan las fechas.


5) Una vez finalizado todo el analisis, en la clase google_GUI_Tkinter, se lanza una consulta a la Database para completar las tablas y poder verlas por pantalla.  


6) Se desconecta de la aplicacion.  



# Detalles sobre la Base de Datos.  [google_Database](https://github.com/NicolasKlaver/Challenge_Meli/blob/main/src/google_Database.py)
- MySQL es un sistema de bases de datos muy potente y versátil que puede manejar una gran cantidad de datos y proporcionar un alto rendimiento y disponibilidad.

- Como explico en el desarrollo del programa, utilizo una sola Database en la cual va a ver muchas Tablas. Dada la estructuracion del codigo, considero que se puede cambiar facilmente si cambia algun requerimiento.
- La idea es que cada usuario tenga dos tablas, una en la que cargaremos todo el Inventario y otro donde guardamos los archivos historicos.
- Uso como nombre de la tabla el user_name del usuario autenticado para poder conectarme en caso de que ya exista.


### Inicializacion

**def __init__(self, user, password, host)**
- Inicializo las variables para conectarme a la Database.
- Inicializo otros parametros que en el futuro usare en todo el programa como "connection", "cursor" y el nombre de las tablas.


### Funciones de Conexion 
**def open_connection(self):** se conecta y inicializa las variables de connection y cursor

**def close_connection(self):** se desconecta

**def select_database(self, db_name):** selecciono la Database a usar.
 

### Funciones de Creacion  

**def create_database(self, db_name):** crea la Database si no existe.

**create_table_inventario(self, table_name):** creo la tabla y inicializo la variable.
  https://github.com/NicolasKlaver/Challenge_Meli/blob/114fc2a93de5c425fe2c9324543e2bb83f4953d1/src/google_Database.py#L172-L179

**create_table_historico(self, table_name):** Creo la tabla y inicializo la variable.
https://github.com/NicolasKlaver/Challenge_Meli/blob/114fc2a93de5c425fe2c9324543e2bb83f4953d1/src/google_Database.py#L216-L222


### Funcion para Agregar Archivos 

**def insertar_archivo_nuevo(self, file, flag_inventario, flag_historico ):** Utilizo la consulta SQL para cada tabla son distintas dado que tienen diferentes columnas, en vez de tener dos funciones distintas decidi unificarlas en una y utilizar flags que me marquen en que tabla voy a insertar el archivo.
  
**Como aclaración, el recurso de los flags lo utilizo varias veces mas, por lo que no voy a explicarlo de nuevo.**


### Funcion de Pedido de Archivos 
**def pedido_archivos(self, flag_inventario, flag_historico):**
- Selecciono todas las filas de las tablas, y guardo los datos mediante un fetchall.
- Creo una lista por comprension con el nombre de las columnas
- Con los datos obtenidos anteriormente, creo y retorno una lista de diccionarios para mantener el formato con el que estuve trabajando.


### Funciones de Actualizacion
- No utilizo ningun recurso nuevo que valga la pena mencionar
  
**def update_time(self, file_id, file_modified_time, flag_inventario, flag_historico)**

**def update_visibility_inventario(self, file_id, file_modified_time)**

### Funcinoes auxiliares 
  - Funciones que devuelven un booleano.

**def existe_archivo(self, file_id, flag_inventario, flag_historico)**

**def fue_modificado(self, file_id, file_last_modified_date)**

**def existe_Database(self, db_name)**



# Detalles sobre la API de Google Drive. [google_DriveAPI](https://github.com/NicolasKlaver/Challenge_Meli/blob/main/src/google_DriveAPI.py)  
- La API de Google Drive es una interfaz de programación de aplicaciones que permite a los desarrolladores interactuar con los archivos y carpetas almacenados en Google Drive. 
- Se utiliza para crear aplicaciones que pueden acceder, modificar y compartir archivos en Google Drive.
- Se basa en el protocolo HTTP y utiliza el formato JSON para enviar y recibir datos.

- Hay distintos Scopes para conectarse. En este caso utilice uno que me permita acceder a todos los archivos con permisos de lectura y escritura ya que puede que tengamos que hacer modificaciones. 


**def __init__(self):**
- Inicializa la clase DriveAPI y define los scopes de acceso para la autenticación de la API de Google Drive.
- Se utiliza un scope que permita acceder a todos los archivos con permisos de lectura y escritura ya que puede que tengamos que hacer modificaciones.

**def authenticate(self):**
- Autenticar a la aplicación para acceder a la API de Google Drive. 
- Si existe un token previamente guardado y no ha expirado, se utiliza ese token. 
- En caso contrario, se solicita la autenticación del usuario y se guarda el token en un archivo local.

    - Se utiliza el metodo 'InstalledAppFlow' de la API de Google, que solicita al usuario que autentique la aplicación en su cuenta de Google para un determinado Scope.
    - Se cargan las credenciales desde un archivo que fue configurado en la Consola de APIs de Google.
    - Estas credenciales se encuentran encriptadas, asique se ejecuta la etapa de desencriptado para obtenerlas.
    - Finalmente, una vez que se ha obtenido el token de acceso, este se almacena en un archivo 'token.pickle' para su uso posterior. 

**def connect(self):**
- Una vez obtenidas las credenciales, se usa la función 'build' que se utiliza para construir un objeto que proporciona acceso a los recursos y métodos de la API de Google Drive.

**def disconnect(self):** se desconecta de la API.

**def get_files(self):**
- Obtener los archivos de Google Drive que cumplan con ciertos criterios de búsqueda. 
- results = self.service.files().list(q=query, fields=fields, pageSize=3).execute()
    - Devuelve una lista de archivos y carpetas que cumplen con los criterios de búsqueda especificados. 

**def get_all_files(self):**
- Devuelve todos los archivos

**def remove_public_visibility(self, file_id):**
- self.service.permissions().delete(fileId= file_id, permissionId='anyoneWithLink').execute()
    - Utilizo la funcion 'delete()' para borrar un permiso a un determinado file_id

**def get_last_modified_date(self, file_id)**
- modified_info = self.service.files().get(fileId= file_id, fields='modifiedTime').execute()
    - Utilizo la funcion get() para obtener el user de la persona que se conectó.

**def get_authenticated_user(self):** devuelve el user autenticado.

**def es_publico(permissions):** recorre una lista de permisos para saber si es publico


# GoogleDriveInventory. [google_DriveInventory.](https://github.com/NicolasKlaver/Challenge_Meli/blob/main/src/google_DriveInventory.py)  
- En esta clase manejo los archivos y hace el flujo de comprobación para cumplir las especificaciones del challenge.
    - En la seccion de  **Explicacion de la estructura del codigo** está explicado en detalle algunas funciones.


### Inicializacion 
**def __init__(self, db, drive_api):**
- objeto de Database: va a ejecutar consultas.
- Objeto de API: ejecuta el pedido de los archivos
- Objeto de Email: manda el mensaje correspondiente.
- Logger

### Funciones para manejar los archivos
**def handler_files(self):**
- Se comunica con GoogleDriveAPI para obtener los archivos y se los manda al proximo método.

**def inventory_files(self, files_list):**
- Recibe los archivos y los envia a su handler correspondiente dependiendo si es un archivo nuevo o viejo.

**def handler_archivos_nuevos(self, file):**
- Inserto en tabla inventario
- Si es publico --> Inserto en la tabla historico y lo mando al handler_visibility

**def handler_archivos_viejos(self, file):**
- Si es publico --> handler_visibility
    - Si no esta en el Historico, lo agrego
- Compruebo si fue modificado "handler_last_modified" 



### Funciones Auxiliares 
**def estaEnInventario(self, file):** consulta SQL por el file_id para saber si existe el file

**def estaEnHistorico(self, file):** consulta SQL por el file_id para saber si existe el file

**def insertar_inventario(self, file):** consulta a SQL para agregar el file

**def insertar_historico(self, file):** consulta a SQL para agregar el file


### Funciones para manejar la Visibilidad y Ultima Modificacion 
**def handler_last_modified(self, file):**
- Hago una consulta a la Database para saber si el archivo fue modificado
- En caso de que esto pase se actualizan los campos.
  
**def handler_visibility(self, file):**
- Hago una consulta a GoogleDrive para remover el estado de Visibilidad 
- Una vez completado, actualizo los campos necesarios de la Database
- Finalmente, envio un mail al owner del archivo.

### Funcion para enviar email 
**def send_email_owner(self, file):** envio un mail con la info del archivo


# google_GUI_Tkinter. [google_GUI_Tkinter](https://github.com/NicolasKlaver/Challenge_Meli/blob/main/src/google_GUI_Tkinter.py)
- Clase que contiene la Interfaz Grafica y el flujo del programa.
- Se inicializan los objetos que van a necesitarse utilizar posteriormente.

### Inicializacion 
- Cargo las credenciales para conectarme a la Database del archivo ".env"
- Inicializa los objetos de los demas modulos (DriveAPI - Database - DriveInventory - Logger)
- Se crean las ventanas principales de la interfaz.


### Graficos 
  - Funciones que crean la Interfaz Grafica.
  
**def crear_ventana_bienvenida()**

**def crear_pestañas()**

**def crear_boton_inicio()**

**def crear_arbol_inventario()**

**def crear_arbol_historico()**


### Alertas 
  - Alertas que informan el desarrollo del programa.
**def alerta_google_drive()**

**def alerta_base_datos()**

**def alerta_archivos_listados()**

**def alerta_finalizacion()**

**def alerta_tablas_completas()**

**def salirAplicacion()**


### Funciones para agregar datos  
- Funciones para completar las tablas de la Interfaz.
  
**def completar_tablas_app():**
- Lanza un pedido de pedido de archivos a la Database.
- Con los resultados continua actualizando la tabla de la interfaz grafica.

**def add_table_inventario(files):** completa la tabla de la interfaz
**def add_table_historico(files):** completa la tabla de la interfaz


### Recorrido del programa 
**def ejecucion_del_programa():** ejecuta en orden cada metodo utilizado.

**def conectarse_google_drive():** empieza el programa conectandose a GoogleDrive.

**def conectarse_a_SQL():** continua la ejecucion creando y conectandose a la Database.

**def crear_tablas_SQL():** continua con la creacion de las tablas.

**def list_google_drive_files():**
- Se conecta con GoogleDriveInventory y empieza el flujo a handler_files para trabajar con los archivos.
- Se queda esperando a que finalice.

**def desconectar_aplicacion():** se desconecta de la API y la Database.

# Google_Email. [google_Email](https://github.com/NicolasKlaver/Challenge_Meli/blob/main/src/google_Email.py)
Clase para enviar correos electrónicos a través de Yagmail.SMTP.
  - Es una librería de Python que proporciona una forma fácil de enviar correos electrónicos a través de Gmail. La librería maneja gran parte de la configuración necesaria en segundo plano, como el servidor SMTP y la autenticación.

### Inicializacion 
**def __init__(self):**
- Carga las variables de entorno desde el archivo .env y obtiene las credenciales de la base de datos desde las variables de entorno. 
- También crea una instancia de  Yagmail.SMTP para el envío de correos electrónicos y una instancia de Logger para el registro de eventos.

**def send_email(self, recipient, subject, body):**
- Envia el email con los datos proporcionados.

# Logger
- Contiene la inicializacion del Logger que nos van a ayudar a verificar como se ejecuto nuestro programa.

**def __init__(self):**
- Inicializa los file_handlers para escribir en el archivo delogs

**def get_logger(self):**
- Devuelve el logger 

# Main. [main](https://github.com/NicolasKlaver/Challenge_Meli/blob/main/src/main.py) 
  - Inicializa la interfaz grafica.


# Tests. [test_general](https://github.com/NicolasKlaver/Challenge_Meli/blob/main/tests/test_general.py)
- Por el momento cuento con los 4 tests que pedia el enunciado.
- El programa lo fui probando a medida que lo fui resolviendo y por error no fui guardando las pruebas. Es una parte que me gustaria tener mas completa pero por un tema de tiempos y organización no llegué.

**def test_connect_drive_and_list_files()**: Se conecta a la API de Google Drive y lista los archivos.


**def test_save_files_in_database()**: Guardar los archivos solicitados en la base de datos.


**def test_change_visibility()**: Cambiar la visibilidad del archivo de público a privado


**def test_email()**: Enviar un correo electrónico al Propietario del archivo, avisando que la visibilidad ha sido cambiada




# Puntos a Revisar
    - Agregar mas messagebox cuando falla el programa. Ahora solo se informa por logs.
    - Darle mas control de la aplicacion al usuario en caso de que se requiera.
    - Analizar usar la libreria smtp para el envío de mails ya que permite una configuración mas personalizada.
    -Revisar las instancias del Logger porque en estos momentos se imprimen multiples.

# Puntos a futuro
  - En el archivo de base de datos se pueden agregar nuevas consultas para hacer un analisis de los datos obtenidos.
    -Por ejemplo, utilizando Joins entre las dos tablas con el "file_id" se pueden obtener los archivos publicos que siguen en la Database y tambien los que fueron eliminados.
    - Una vez conectado el usuario se podria hacer una consulta a SQL y mostrandole al usuario los archivos que tenia antes de iniciar nuevamente el programa.
    - Se puede mejorar la logica de la Creacion de tablas, ya que aunque la funcion se llamen "create_table", si no existe, no las crea, pero lo que si hace es asignarle el nombre que es importante para trabajar posteriormente.
   
