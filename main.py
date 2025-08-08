import os
import time
from processor import procesar_archivo
from config import INPUT_FOLDER, PROCESSED_FOLDER, ERROR_FOLDER, LOG_FOLDER
from logger import configurar_logger

logger = configurar_logger()

def main():
    print("Rutas configuradas:")
    print(f"Entrada:     {INPUT_FOLDER}")
    print(f"Procesados:  {PROCESSED_FOLDER}")
    print(f"Errores:     {ERROR_FOLDER}")
    print(f"Logs:        {LOG_FOLDER}")

    logger.info("Iniciando monitor de archivos...")

    while True:
        archivos = [f for f in os.listdir(INPUT_FOLDER) if os.path.isfile(os.path.join(INPUT_FOLDER, f))]

        for archivo in archivos:
            logger.info(f"Detectado archivo: {archivo}")
            procesar_archivo(archivo)
        
        time.sleep(5)

def crear_carpetas_si_no_existen():
    for carpeta in [PROCESSED_FOLDER, ERROR_FOLDER, LOG_FOLDER]:
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

if __name__ == "__main__":
    main()