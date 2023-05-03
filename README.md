# Challenge_Meli

Instalar bibliotecas para ejecutar:
pip install google-api-python-client
pip install mysql-connector-python

# Estructuras de las carpetas
Challenge_Meli:
    -src:
      - google_Database: contiene en la clase "Database" toda la lógica relacionada con la Base de Datos.
      - google_DriveAPI: contiene en la clase "GoogleDriveAPI" toda la logica relacionado con la API de google drive.
      - google_DriveInventory: contiene en la clase "GoogleDriveInventory" la lógica para analizar y manipular los archivos obtenidos de google drive.
      - google_Email: contiene en la clase "EmailNotifier" la logica para enviar correos electronicos.
      - google_GUI_Tkinter: contiene la clase "App" donde se encuentra la parte de la Interfaz Grafica y la lógica para ejecutar el programa.
      - logger: contiene la clase "Logger" que se utiliza para imprimir los logs correspondientes.
      - main: contiene la ejecucion del programa.
    
    - Logs:
      - log_info: contiene los logs de la ejecucion.
    
    - Tests:
      - test_general: contienen los tests para probar el programa.
  
    - Config:
      - credential_drive.json
      - .env: archivo con las variables y contraseñas.

##################################################################################################################
# Aclaraciones acerca de la construccion y el objetivo del programa.
    - Realice el programa pensando que trabajo en el área de Seguridad Informática, y que el objetivo es tratar con archivos sensibles que pueden llegar a ser publicos. 
    - Por eso, como podras ver mas adelante, el usuario no tiene relación ni elección con la ejecución del programa, si no que se le deberá explicar de que se trata y ejecutarlo en caso de que este de acuerdo.
   




  # Explicacion de la estructura del codigo

1) El archivo "google_GUI_Tkinter.py" ejecuta la interfaz gráfica y una vez el usuario haga click en el boton "Iniciar Programa" saldrá un mensaje de alerta el cual deberá aceptar.
2) Una vez aceptado, se lanza un pedido para conectarse a Google Drive, en caso de que sea exitoso, se crea una Base de Datos(*1*) y se selecciona para poder trabajar con ella.
   Una vez conectado, se crean dos tablas: una para el Inventario en general, y otra para el historico (*2). Se utiliza el nombre del owner de la cuenta que lo obtenemos haciendole un pedido a GoogleDriveAPI.

*1* En este caso creo una base de datos general para todos los usuarios y multiples tablas por cada uno, pero es un requirimiento que facilmente puede cambiar por eso llamo a la funcion "create_database" aunque solo la utilice una vez. **

*2* Para este caso no considero que sea necesaria tener dos tablas, ya que la tabla inventario contiene un parámetro que informa si un archivo fue público. Pero considerando que en un futuro se pueda sumar lógica para sacar de la tabla archivos eliminados, en este caso utilizo una tabla como back-up para no perder la información de los archivos que alguna vez fueron públicos.


3) La ejecución sigue en el archivo "google_DriveInventory.py" donde hago un pedido a la clase de Google Drive para listar los archivos con el metodo "handler_files". 
4) Una vez obtenidos con exito, analizo en un for un archivo a la vez con el metodo "inventory_files". Lo primero que hago es ver si se encuentran en el Inventario.
  4.1) Analisis con archivos que NO estan en el Inventario, metodo "handler_archivos_nuevos".
    - Inserto el archivo en la Database.
    - Si ademas, el archivo es publico:
      -  Lo cargo en el Historico.
      -  "handler_visibility": Lanzo una solicitud a GoogleDriveAPI para cambiar la Visibilidad. Una vez hecho este cambio, hago una consulta para obtener la hora de la ultima modificación hecha y actualizo la visibilidad a la tabla Inventario y la hora de modificacion a ambas tablas(*3*).
   - Finalmente mando un email al usuario indicando el cambio.

(*3*) Esta logica creo que se puede mejorar o cambiar, sobre todo si le diera mas libertad al usuario para ver sus cosas. 
En esta caso estoy cargando un archivo nuevo con Visibilidad publica y en el mismo transcurso del programa lo actualizo a privado. 


  4.2) Archivos que estan en el inventario, metodo "handler_archivos_viejos".
    - Si el archivo es publico, lo cargo en el histórico en caso de que no este y llamo como arriba al metodo handler_visibility.
    - Si no es publico, chequeo si fue modificado lanzando una consulta a la Database y comparando la hora con la actual, con el metodo "handler_last_modified". En caso que que corresponda se actualizan las fechas.

5) Una vez finalizado todo el analisis, en la clase google_GUI_Tkinter, se lanza una consulta a la Database para completar las tablas y poder verlas por pantalla.

6) Se desconecta de la aplicacion.


# ------------------------------------------------------------------------------------
# Detalles sobre la Base de Datos
- MySQL es un sistema de bases de datos muy potente y versátil que puede manejar una gran cantidad de datos y proporcionar un alto rendimiento y disponibilidad.

def __init__(self, user, password, host)
- Inicializo las variables para conectarme a la Database.
- Además en este metodo guardo los nombres de las tablas:
######################self.table_inv= None
######################self.table_historico= None
La idea es que cada usuario tenga dos tablas y uso como identificador unico el user_name para que no se puedan repetir.
Como explico en el desarrollo del programa, utilizo una sola Base de Datos y es un requerimiento que se puede cambiar facilmente.

- Ahora veamos los metodos: voy a explicar mas en detalle los que considero mas complicados de entender y nombrar los que son mas simples para que no queda muy extenso.
  

** Funciones de Conexion **
open_connection:
    - Utilizo el metodo mysql.connector.connect con las variables del inicio para conectarme y guardar esta conexion que es la que usaré todo el programa.
 
 close_connection: se hace mediante la funcion close()



** Funciones de Creacion  **

create_database:
create_table_inventario(table_name):
    - Cuando creo la tabla inicializo para la clase el nombre de la tabla(self.table_inv)
#############################################
create_table_historico(table_name):
    - - Cuando creo la tabla inicializo para la clase el nombre de la tabla(self.table_historico)



** Funcion de Insertar Archivos  **
###########  def insertar_archivo_nuevo(self, file, flag_inventario, flag_historico )
- La consulta a SQL para cada tabla son distintas dado que tienen diferentes columnas, pero en vez de tener don funciones distintas decidi unificarlas en una y utilizar flags que me marquen a que tabla voy a insertar el archivo.
  
**Como aclaración, el recurso de los flags lo utilizo varias veces mas, por lo que no voy a explicarlo de nuevo.**

** Funcion de Pedido de Archivos **
    - Selecciono todo de las tablas, y obtengo los datos mediante un fetchall
    - #################################
    - Creo una lista por comprension con el nombre de las columnas
    - #################################
    - Creo y retorno una lista de diccionario para mantener el formato con el que estuve trabajando.


** Funciones de Actualizacion **
- No utilizo ningun recurso nueo que valga la pena mencionar
def update_time_inventario(self, file_id, file_modified_time, flag_inventario, flag_historico)

def update_visibility_inventario(self, file_id, file_modified_time):

** FUNCION AUXILIARES PARA BUSCAR EN LA BASE DE DATOS ** 
def existe_archivo(self, file_id, flag_inventario, flag_historico)

def fue_modificado(self, file_id, file_last_modified_date)

 def existe_Database(self, db_name)


Cosas a agregar:
    - Una vez conectado el usuario se podria hacer una consulta a SQL y mostrandole al usuario los archivos que tenia antes de iniciar nuevamente el programa.
    - Se puede mejorar la logica de la Creacion de tablas, ya que aunque la funcion se llamen "create_table", si no existe, no las crea, pero lo que si hace es asignarle el nombre que es importante para trabajar posteriormente.
    - 



# -------------------------------------------------------------------------------------
# Detalles sobre la API de Google Drive
- La API de Google Drive es una interfaz de programación de aplicaciones que permite a los desarrolladores interactuar con los archivos y carpetas almacenados en Google Drive. - Esta API se utiliza para crear aplicaciones que pueden acceder, modificar y compartir archivos en Google Drive.
- La API de Google Drive se basa en el protocolo HTTP y utiliza el formato JSON para enviar y recibir datos.

- Hay distintos Scopes para conectarse. En este caso utilice uno que me permita acceder a todos los archivos con permisos de lectura y escritura ya que puede que tengamos que hacer modificaciones.
1) Lo primero que hay que hacer es obtener las credenciales de autenticación,
  -  Primero verifica si ya se ha obtenido un token de acceso.
  - Si no se habia obtenido, se utiliza el metodo 'InstalledAppFlow' de la API de Google, que solicita al usuario que autentique la aplicación en su cuenta de Google para un determinado Scope.
  - El método necesita para ejecutarse correctamente tener las credenciales de la aplicación desde un archivo que debe haber sido previamente configurado en la Consola de APIs de Google.
  - Finalmente, una vez que se ha obtenido el token de acceso, este se almacena en un archivo 'token.pickle' para su uso posterior. 

2) Una vez obtenidas las credenciales, se usa la función 'build' que se utiliza para construir un objeto que proporciona acceso a los recursos y métodos de la API de Google Drive.

3) Una vez conectado podemos hacer las consultas que queramos, para este programa particular:
Siendo "self.service" el objeto mencionado anteriormente:
    
    - Utilizo la función 'list()  para obtener una lista de archivos y carpetas que cumplen con los criterios de búsqueda especificados. 
results = self.service.files().list(q=query, fields=fields, pageSize=3).execute()

    - Utilizo la funcion 'delete()' para borrar un permiso a un determinado file_id
  self.service.permissions().delete(fileId= file_id, permissionId='anyoneWithLink').execute()

    - Utilizo la funcion get() para obtener el user de la persona que se conectó.
 user_info = self.service.about().get(fields='user(emailAddress)').execute()
# -------------------------------------------------------------------------------------


## Puntos que se pueden mejorar:
    - Mejorar los tests --> Crear modelos para listar los archivos y generar mas pruebas.


    - Agregar mas messagebox cuando falla el programa --> Ahora solo se informa por logs
    - Darle mas control de la aplicacion al usuario en caso de que se requiera
    - Separar de la clase App la parte de Interfaz grafica y ejecucion del progranma en una nueva clase.
  