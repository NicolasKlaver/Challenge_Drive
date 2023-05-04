import mysql.connector
import datetime
from logger import Logger


class Database:
    """
    Clase para conectarse a una base de datos MySQL y ejecutar consultas SQL.

    Raises:
        err: _description_
        err: _description_
        err: _description_
        err: _description_
        err: _description_

    Returns:
        _type_: _description_
    """
    ########## FUNCION DE INICIALIZACION ##########
    def __init__(self, user, password, host):
        """
        Constructor de la clase BaseDeDatos
        
        Args:
            user (str): Nombre de usuario para conectarse a la base de datos.
            password (str): Contraseña para conectarse a la base de datos.
            host (str): Dirección IP o nombre de host del servidor de la base de datos.

        Returns: None
        """
        self.user = user
        self.password = password
        self.host = host
        self.connection = None
        self.cursor = None
        self.table_inv= None
        self.table_historico= None
        #self.logger = Logger().get_logger()
        self.logger= None


    ########## FUNCION DE CONEXION ##########
    def open_connection(self):
        """
        Opens a connection to a MySQL database using the provided credentials.

        Returns: None

        Raises:
            mysql.connector.Error: if the connection cannot be established
        """
        try:
            # Establece la conexión con la base de datos MySQL
            self.connection = mysql.connector.connect(
                user=self.user,
                password=self.password,
                host=self.host
            )
            
            # Creates a cursor object to execute SQL queries
            self.cursor = self.connection.cursor()
            
            self.logger.info("Conectado a MySQL con éxito")
            print("Conectado a MySQL con éxito")
            
        except mysql.connector.Error as e:
            self.logger.error(f"Error al conectar a la base de datos: {e}")
            raise
        
    def close_connection(self):
        """
        Closes the connection to the MySQL database and the cursor.

        Returns: None

        Raises:
            Exception: if an error occurs while closing the connection or cursor.
        """
        
        try:
            # Si el cursor no es nulo, se cierra.
            if self.cursor is not None:
                self.cursor.close()
            # Si la conexión no es nula, se cierra.
            if self.connection is not None:
                self.connection.close()
            self.logger.info("Desconectado a MySQL con éxito")
        except Exception as e:
            self.logger.error(f"Error al cerrar la conexion a la base de datos: {e}")
        
        
    ########## FUNCION DE CRACION DE BASE DE DATOS Y TABLAS ##########
    def create_database(self, db_name):
        """
        Creates a new database with the provided name if it doesn't already exist.

        Args:
            db_name (str): The name of the database to create.

        Returns: None

        Raises:
            mysql.connector.Error: if there is an error creating the database
        """
        
        #Compruebo si la base de datos existe
        result= self.existe_Database(db_name)
        
        if result:
            self.logger.info("La base de datos ya existe.")
            print("La base de datos ya existe.")
        
        else:
            try:
                # Creates a cursor object to execute SQL queries
                #self.cursor = self.connection.cursor()
                # SQL query to create the database
                sql= "CREATE DATABASE IF NOT EXISTS {db_name}".format(db_name=db_name)
                # Executes the SQL query
                self.cursor.execute(sql)
                
                self.logger.info("La base de datos se ha creado exitosamente.")
                print("La base de datos se ha creado exitosamente.")
            
            # If there is an error, prints the error message
            except mysql.connector.Error as err:
                print(f"Error al crear la base de datos: {err}")
                self.logger.error(f"Error al crear la base de datos: {err}")
                                
    def select_database(self, db_name):
        """
        Changes the currently selected database to the provided name.

        Args:
            db_name (str): The name of the database to select.

        Returns: None

        Raises:
            mysql.connector.Error: if there is an error connecting to the database.
        """
        try:
            # Cambia la base de datos seleccionada en la conexión actual
            self.connection.database = db_name
            self.logger.info(f"La base de datos: {db_name} se ha seleccionado correctamente.")
        except mysql.connector.Error as err:
            print(f"Error al conectarse a la base de datos: {err}")
            self.logger.error(f"Error al conectarse a {db_name}: {err}")
              
    def create_table_inventario(self, table_name):
        """
        Crea una tabla de inventario en la base de datos actual.

        Args:
            table_name (str): El nombre de la tabla a crear.

        Returns: None

        Raises:
            mysql.connector.Error: Si hay algún error al crear la tabla.

        """
        #Asigno el valor del nombre de la tabla 
        self.table_inv = table_name
        print("\nTabla inventario: ",  self.table_inv)

        try:
            # Obtenemos un cursor para la conexión actual
           # self.cursor = self.connection.cursor()
            # Definimos la consulta SQL para crear la tabla
            sql = """CREATE TABLE IF NOT EXISTS {} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                file_id VARCHAR(100),
                name VARCHAR(255),
                extension VARCHAR(100),
                owner VARCHAR(255),
                visibility ENUM('publico', 'privado'),
                fecha_ultima_modificacion DATETIME
              )""".format(self.table_inv)
            
            # Ejecutamos la consulta SQL para crear la tabla
            self.cursor.execute(sql)
            
            #Comprobamos si la ultima consulta afecto a alguna fila
            if self.cursor.rowcount == -1:
                print(f"La Tabla {self.table_inv} ya existe.")
                self.logger.info(f"La Tabla {self.table_inv} ya existe.")       
            else:
                print(f"La tabla {self.table_inv} se ha creado exitosamente.")
                self.logger.info(f"La tabla {self.table_inv} se ha creado exitosamente.")
                    
        except mysql.connector.Error as err:
            print(f"Error al crear la tabla: {err}")  
            self.logger.error(f"Error al crear la tabla: {err}")  
    
    def create_table_historico(self, table_name):
        """
        Crea una tabla historica en la base de datos actual.

        Args:
            table_name (str): El nombre de la tabla a crear.

        Returns: None

        Raises:
            mysql.connector.Error: Si hay algún error al crear la tabla.

        """
        self.table_historico = table_name
        print("\n\nTabla Historico: ",  self.table_historico)
        try: 
            # Obtenemos un cursor para la conexión actual
          #  self.cursor = self.connection.cursor()
            # Definimos la consulta SQL para crear la tabla
            sql = """CREATE TABLE IF NOT EXISTS {} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                file_id VARCHAR(100),
                name VARCHAR(255),
                extension VARCHAR(100),
                owner VARCHAR(255),
                fecha_ultima_modificacion DATETIME
              )""".format(self.table_historico)
            
            # Ejecutamos la consulta SQL para crear la tabla
            self.cursor.execute(sql)
            
            #Comprobamos si la ultima consulta afecto a alguna fila
            if self.cursor.rowcount == -1:
                print(f"La Tabla {self.table_historico} ya existe.")
                self.logger.info(f"La Tabla {self.table_historico} ya existe.")       
            else:
                print(f"La tabla {self.table_inv} se ha creado exitosamente.")
                self.logger.info(f"La tabla {self.table_inv} se ha creado exitosamente.")
            
        except mysql.connector.Error as err:
            print(f"Error al crear la tabla: {err}")   
            self.logger.error(f"Error al crear la tabla: {err}")
    
    
    ########## FUNCION PARA INSERTAR ARCHIVOS EN LA BASE DE DATOS ##########
    def insertar_archivo_nuevo(self, file, flag_inventario, flag_historico ):
        """
        Inserta un nuevo archivo en la tabla 'inventario'.

        Args:
            file: Un diccionario que contiene la información del archivo a insertar.
            flag_inventario: Un booleano que indica si se debe insertar el archivo en la tabla 'inventario'.
            flag_historico: Un booleano que indica si se debe insertar el archivo en la tabla 'historico'.
        Returns:None

        Raises:
            mysql.connector.Error: Si ocurre un error al insertar el archivo en la tabla 'inventario'.
        """

        try:
            # Cambio de formato la fecha
            file_modified_time = datetime.datetime.strptime(file['modified_time'], '%Y-%m-%dT%H:%M:%S.%fZ')

            # Crear el cursor
            # self.cursor = self.connection.cursor()    
            
            # Definimos la consulta SQL para crear la tabla
            sql_inventario= f"INSERT INTO {self.table_inv} (file_id, name, extension, owner, visibility, fecha_ultima_modificacion) VALUES (%s, %s, %s, %s, %s, %s)"
            #Creamos una tupla con los valores a insertar
            values_inventario = (file['id'], file['name'], file['extension'],file['owner'], file['visibility'],file_modified_time)
            
            # Definimos la consulta SQL para crear la tabla
            sql_historico= f"INSERT INTO {self.table_historico} (file_id, name, extension, owner, fecha_ultima_modificacion) VALUES (%s, %s, %s, %s, %s)"

            #Creamos una tupla con los valores a insertar
            values_historico = ( file['id'], file['name'], file['extension'],file['owner'],file_modified_time)
            
            
            if flag_inventario:
            # Ejecutamos la consulta SQL para crear la tabla
                self.cursor.execute(sql_inventario, values_inventario)
                flag_inventario=0
                self.logger.info(f"Se ha insertado {file['name']} en el Inventario exitosamente.") 
                
            if flag_historico:
            # Ejecutamos la consulta SQL para crear la tabla
                self.cursor.execute(sql_historico, values_historico)
                flag_historico=0   
                self.logger.info(f"Se ha insertado {file['name']} en el Historico exitosamente.") 

            
            # Guardamos los cambios
            self.connection.commit()
                      
        
        except mysql.connector.Error as err:
            print(f"Error al insertar el archivo: {err}")
            self.logger.error(f"Error al insertar el archivo: {err}")

    ########## FUNCION PARA INSERTAR ARCHIVOS EN LA BASE DE DATOS ##########
    def insertar_archivo_test(self, file):
        """
        Inserta un nuevo archivo en la tabla 'test'.

        Args:
            file: Un diccionario que contiene la información del archivo a insertar.
        Returns:None

        Raises:
            mysql.connector.Error: Si ocurre un error al insertar el archivo en la tabla 'inventario'.
        """

        try:
            # Cambio de formato la fecha
            file_modified_time = datetime.datetime.strptime(file['modified_time'], '%Y-%m-%dT%H:%M:%S.%fZ')

            # Crear el cursor
            self.cursor = self.connection.cursor()    
            
            # Definimos la consulta SQL para crear la tabla
            sql= f"INSERT INTO Test_Inventario (file_id, name, extension, owner, visibility, fecha_ultima_modificacion) VALUES (%s, %s, %s, %s, %s, %s)"
            #Creamos una tupla con los valores a insertar
            values = (file['id'], file['name'], file['extension'],file['owner'], file['visibility'],file_modified_time)

            # Ejecutamos la consulta SQL para crear la tabla
            self.cursor.execute(sql, values)
            self.logger.info(f"Se ha insertado {file['name']} en el Inventario exitosamente.") 
                 
            # Guardamos los cambios
            self.connection.commit()
                      
        
        except mysql.connector.Error as err:
            print(f"Error al insertar el archivo: {err}")
            self.logger.error(f"Error al insertar el archivo: {err}")

    def eliminar_table(self, table_name):
        """
        

        Args:
            file: Un diccionario que contiene la información del archivo a insertar.
        Returns:None

        Raises:
            mysql.connector.Error: Si ocurre un error al insertar el archivo en la tabla 'inventario'.
        """

        try:
            # Crear el cursor
            self.cursor = self.connection.cursor()    
            
            # Definimos la consulta SQL para crear la tabla
            sql= "DROP TABLE IF EXISTS {}".format(table_name)
            #Creamos una tupla con los valores a insertar

            # Ejecutamos la consulta SQL para crear la tabla
            self.cursor.execute(sql)
            print(f"Se ha eliminado la tabla: {table_name} en el Inventario exitosamente.")
            self.logger.info(f"Se ha eliminado la tabla: {table_name} en el Inventario exitosamente.") 
                 
            # Guardamos los cambios
            self.connection.commit()
                      
        except mysql.connector.Error as err:
            print(f"Error al insertar el archivo: {err}")
            self.logger.error(f"Error al insertar el archivo: {err}")
    
    ########## FUNCION QUE DEVUELVE LOS ARCHIVOS  ##########
    def pedido_archivos(self, flag_inventario, flag_historico):
        """
        Consulta en SQL para seleccionar todos los datos de la tabla correspondiente.
        
        Args: 
            flag_inventario: Un booleano que indica si se debe seleccionar el archivo en la tabla 'inventario'.
            flag_historico: Un booleano que indica si se debe seleccionar el archivo en la tabla 'historico'.
            
        Returns: lista de diccionarios, donde cada diccionario representa un archivo en el inventario.

        Raises:
            mysql.connector.Error: Si ocurre un error al seleccionar los datos en la tabla.
        """
        
        try:
            # Crear el cursor
            #self.cursor = self.connection.cursor()
            
            # Definimos la consulta SQL para seleccionar los datos de la tabla
            sql_inventario = f"SELECT * FROM {self.table_inv}"
            
            # Definimos la consulta SQL para seleccionar los datos de la tabla
            sql_historico = f"SELECT * FROM {self.table_historico}"
            
            if flag_inventario:
                # Ejecutamos la consulta SQL
                self.cursor.execute(sql_inventario)
                
            elif flag_historico:
                self.cursor.execute(sql_historico)
                

            # Obtener los datos de la consulta y crear una lista de diccionarios
            rows= self.cursor.fetchall()
            # Se guardan los nombres de las columnas
            columns = [desc[0] for desc in self.cursor.description]
            
            self.logger.info(f"Se ha hecho un pedido de archivos historicos exitosamente.")
            
            # Devuelve una lista de diccionarios, donde cada diccionario representa un archivo en el inventario
            return [dict(zip(columns, row)) for row in rows]
        
        except mysql.connector.Error as err:
            # En caso de error, imprimir el mensaje correspondiente
            print(f"Error al seleccionar los datos: {err}")
            self.logger.error(f"Error al seleccionar los datos de la tabla: {self.table_inv} {err}")
    
    def pedido_archivos_test(self):
        """
        Consulta en SQL para seleccionar todos los datos de la tabla correspondiente.
        
        Args: 
            flag_inventario: Un booleano que indica si se debe seleccionar el archivo en la tabla 'inventario'.
            flag_historico: Un booleano que indica si se debe seleccionar el archivo en la tabla 'historico'.
            
        Returns: lista de diccionarios, donde cada diccionario representa un archivo en el inventario.

        Raises:
            mysql.connector.Error: Si ocurre un error al seleccionar los datos en la tabla.
        """
        
        try:
            # Crear el cursor
            self.cursor = self.connection.cursor()
            
            # Definimos la consulta SQL para seleccionar los datos de la tabla
            sql = f"SELECT * FROM Test_Inventario"
            self.cursor.execute(sql)                

            # Obtener los datos de la consulta y crear una lista de diccionarios
            rows= self.cursor.fetchall()
            # Se guardan los nombres de las columnas
            columns = [desc[0] for desc in self.cursor.description]
            
            self.logger.info(f"Se ha hecho un pedido de archivos historicos exitosamente.")
            
            # Devuelve una lista de diccionarios, donde cada diccionario representa un archivo en el inventario
            return [dict(zip(columns, row)) for row in rows]
        
        except mysql.connector.Error as err:
            # En caso de error, imprimir el mensaje correspondiente
            print(f"Error al seleccionar los datos: {err}")
            self.logger.error(f"Error al seleccionar los datos de la tabla: {err}")
        
    ########## FUNCION AUXILIARES PARA BUSCAR EN LA BASE DE DATOS ##########
    def existe_archivo(self, file_id, flag_inventario, flag_historico):
        """
        Comprueba si un archivo con el ID especificado ya existe en la tabla del inventario.

        Args:
            file_id (str): El ID del archivo a comprobar.

        Returns:
            bool: True si el archivo existe en la tabla, False en caso contrario.

        Raises:
            mysql.connector.Error: Si ocurre algún error al realizar la consulta SQL.
        """
        try:
            # self.cursor = self.connection.cursor()
        
            # Definimos la consulta SQL 
            sql_inventario = f"SELECT * FROM {self.table_inv} WHERE file_id=%s"
            sql_historico = f"SELECT * FROM {self.table_historico} WHERE file_id=%s"
           
            
            if flag_inventario:
                # Ejecutamos la consulta SQL
                self.cursor.execute(sql_inventario, (file_id,))
            
            elif flag_historico:
                # Ejecutamos la consulta SQL
                self.cursor.execute(sql_historico, (file_id,))
            
            # Obtener los datos de la consulta
            result= self.cursor.fetchall()
            
            self.logger.info(f"Se ha comprobado si existe el archivo.")       
   
            # Devuelve True si el archivo existe en la tabla, False en caso contrario
            return bool(len(result))
        
        except mysql.connector.Error as err:
            print(f"Error al comprobar la existencia del archivo: {err}")
            self.logger.error(f"Error al comprobar la existencia del archivo: {err}")
            raise err

    def fue_modificado(self, file_id, file_last_modified_date):
        """
        Comprueba si un archivo ha sido modificado después de la fecha proporcionada.

        Args:
            file_id (str): El ID del archivo a comprobar.
            file_last_modified_date (datetime.datetime): Fecha de la última modificación del archivo.

        Returns:
            bool: True si el archivo ha sido modificado después de la fecha proporcionada, False de lo contrario.
        """
        try: 
            # Definimos la consulta SQL 
            sql= f"SELECT fecha_ultima_modificacion FROM {self.table_inv} WHERE file_id=%s"
            # Ejecutamos la consulta SQL
            self.cursor.execute(sql, (file_id,))
            
            # obtiene la fecha de la última modificación de un archivo que se encuentra en la base de datos
            ultima_modificacion= self.cursor.fetchone()[0]
            
            self.logger.info("Se analiza si el archivo fue modificado correctamente.")
            
            return file_last_modified_date > ultima_modificacion 
        
        except mysql.connector.Error as err:
            print(f"Error al comprobar la ultima fecha de modificacion: {err}")
            self.logger.error(f"Error al comprobar la ultima fecha de modificacion: {err}")
            raise err

    def existe_Database(self, db_name):
        """
        Checks if a given database exists in the MySQL server.

        Args:
            db_name (str): The name of the database to check.

        Returns:
            bool: True if the database exists, False otherwise.
        """
        # Se crea un cursor para ejecutar comandos SQL en la conexión
        #self.cursor = self.connection.cursor()
        # Se ejecuta el comando para obtener la lista de bases de datos
        self.cursor.execute("SHOW DATABASES")
        # Se obtiene la lista de bases de datos y se guarda en la variable databases
        databases = [db[0] for db in self.cursor.fetchall()]
        
        # Se verifica si el nombre de la base de datos se encuentra en la lista de bases de datos
        return db_name in databases

    ########## FUNCIONES DE UPDATES ########## DOCSTRING
    def update_time(self, file_id, file_modified_time, flag_inventario, flag_historico):
        """
        Actualiza la fecha ntario.
        Args:
            file_id (str): El ID del archivo a actualizar.
            file_modified_time (datetime.datetime): La nueva fecha de última modificación del archivo.
            flag_inventario (bool): True si se quiere actualizar la tabla inventario, False en caso contrario.
            flag_historico (bool): True si se quiere actualizar la tabla historico, False en caso contrario.
        Raises:
            mysql.connector.Error: Si ocurre algún error al realizar la consulta SQL.
        """
        try: 
            #self.cursor = self.connection.cursor()
            
            # Definimos la consulta SQL y los valores
            sql_inventario= f"UPDATE {self.table_inv} SET fecha_ultima_modificacion=%s WHERE file_id=%s"
            sql_historico= f"UPDATE {self.table_historico} SET fecha_ultima_modificacion=%s WHERE file_id=%s"
           
            values= (file_modified_time, file_id)
            
            if flag_inventario:
                # Ejecutamos la consulta SQL
                self.cursor.execute(sql_inventario, values)
                self.logger.info(f"Se ha Actualizado el archivo inventario correctamente.")       
            
            elif flag_historico:
                self.cursor.execute(sql_historico, values)
                self.logger.info(f"Se ha Actualizado el archivo historico correctamente.")  
            
            # Guardamos los cambios
            self.connection.commit()
     
        except mysql.connector.Error as err:
            self.logger.error(f"Error al update: {err}")

            raise err
            
    def update_visibility_inventario(self, file_id, file_modified_time):
        """
        Actualiza la visibilidad y la fecha de última modificación de un archivo en el inventario.

        Args:
            file_id (str): El ID del archivo a actualizar.
            file_modified_time (datetime): La fecha de última modificación del archivo.

        Raises:
            mysql.connector.Error: Si ocurre algún error al realizar alguna de las consultas SQL.
        """
        try:
            #self.cursor = self.connection.cursor()
            new_visibility= "privado"
            
            # Definimos la consulta SQL, valores y ejecutamos la consulta
            sql1= f"UPDATE {self.table_inv} SET visibility=%s WHERE file_id=%s"
            values= (new_visibility, file_id)
            self.cursor.execute(sql1, values)
            
            # Definimos la consulta SQL, valores y ejecutamos la consulta
            sql2= f"UPDATE {self.table_inv} SET fecha_ultima_modificacion=%s WHERE file_id=%s"
            values= (file_modified_time, file_id)
            self.cursor.execute(sql2, values)

            #Guarda los cambios
            self.connection.commit()
            self.logger.info(f"Se ha actualizado la visibilidad del archivo en la DB correctamente.")       
   
            
        except mysql.connector.Error as err:
            print(f"Error al comprobar la existencia del archivo: {err}")
            self.logger.error(f"Error al update visibility: {err}")
            raise err



#db= Database("root", "root", "localhost")
#db.open_connection()
#db.select_database("inventario_drive")

#file= {'id':"123", 'name':"archivo", 'extension':"pdf", 'owner':'nicooklaver@gmail.com','modified_time':"2022-09-26T05:50:23.917Z"}

#db.insertar_archivo_nuevo(file, flag_inventario=0, flag_historico=1)


