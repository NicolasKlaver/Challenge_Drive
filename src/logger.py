import logging

class Logger:
    def __init__(self):
        """
        Inicializa un objeto Logger con un nivel de registro y un archivo de registro.

        Args:
            level (str): Nivel de registro (DEBUG, INFO, WARNING, ERROR, CRITICAL). Predeterminado es 'INFO'.
            filename (str): Nombre del archivo de registro. Predeterminado es 'log_info.log'.

        Returns: None
        """
        level='INFO'
        filename='logs/log_info.log'
        
        self.logger = logging.getLogger(filename)
        self.logger.setLevel(level.upper())

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        file_handler = logging.FileHandler(filename)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        """
         Devuelve el logger configurado para escribir en un archivo y en la consola.

        Returns:
            logging.Logger: Logger configurado.
        """
        return self.logger