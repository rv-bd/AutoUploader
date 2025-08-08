import os

DIRECCION = os.path.join(os.path.expanduser("~"), "Desktop") #Cambiar la palabra Desktop por Escritorio dependiendo del lenguaje del servidor

DIRECCION_PROCESADOS = os.path.join(os.path.expanduser("~"), "Documents") #Cambiar la palabra Documents por Documentos dependiendo del lenguaje del servidor

INPUT_FOLDER = os.path.join(DIRECCION, "FTP")
PROCESSED_FOLDER = os.path.join(DIRECCION_PROCESADOS, "procesados")
ERROR_FOLDER = os.path.join(DIRECCION_PROCESADOS, "errores")
LOG_FOLDER = "logs"

MAX_BATCH_SIZE = 5000

DB_CONFIG = {
    "host": "",
    "user": "",
    "password": "",
    "database": "",
    "port": 3306
}

DB_CONFIG_LOCAL = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "desarrollo",
    "database": "isflo",
    "port": 3306
}