from db import execute_stored_procedure
from tqdm import tqdm
import logging
import time

logger = logging.getLogger(__name__)

def ejecutar_procedimientos(info, fecha_param, mover_a_error_fn=None, archivo=None):
    procedimientos = info.get("procedimientos", [])

    barra = tqdm(procedimientos, desc="Procedimientos", unit="proc")
    for proc in barra:
        nombre = proc["nombre"]
        usa_param = proc.get("usa_parametro", False)

        barra.set_description(f"Ejecutando: {nombre}")
        inicio = time.time()

        try:
            if usa_param:
                execute_stored_procedure(nombre, args=(fecha_param,))
            else:
                execute_stored_procedure(nombre)
        
            duracion = time.time() - inicio 
            logger.info(f"Procedimiento ejecutado: {nombre} | Parámetro: {fecha_param if usa_param else 'N/A'} | Duracion: {duracion:.2f} segundos")
        except Exception as e:
            logger.error(f"Error ejecutando procedimiento '{nombre}': {e}")
            if mover_a_error_fn and archivo:
                mover_a_error_fn(archivo)
            raise e