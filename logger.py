import os
import logging
from datetime import datetime
from config import LOG_FOLDER

def configurar_logger():
    if not os.path.exists(LOG_FOLDER):
        os.makedirs(LOG_FOLDER)
    
    fecha_actual = datetime.now().strftime('%Y%m%d')
    log_path= os.path.join(LOG_FOLDER, f"log_{fecha_actual}.log")

    logger = logging.getLogger("procesador")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.INFO)
        file_format = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter('[%(levelname)s] %(message)s')
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)

    return logger