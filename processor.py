import os
import re
import csv
import shutil
import yaml
from db import insert_into_table, execute_stored_procedure, borrar_registros_por_valores
from config import INPUT_FOLDER, PROCESSED_FOLDER, MAX_BATCH_SIZE, ERROR_FOLDER
from logger import configurar_logger
from datetime import datetime
from utils.campos_dinamicos import(
    ordenar_columnas_calculadas,
    incluir_columnas_calculadas
)
from utils.pre_procesamiento import ejecutar_borrado_previo
from utils.post_procesamiento import ejecutar_procedimientos

logger = configurar_logger()
ARCHIVO_TABLA_MAP = {}

with open("archivo_tabla_map.yaml", "r", encoding="utf-8") as f:
    ARCHIVO_TABLA_MAP = yaml.safe_load(f)

def extraer_prefijo(nombre_archivo):
    match = re.match(r"^(.*)_\d{8}\.csv$", nombre_archivo)

    if match:
        return match.group(1)
    return None

def extraer_fecha_yyyymm(nombre_archivo):
    match = re.match(r"^(.*)_(\d{8})\.csv$", nombre_archivo)
    if match:
        fecha_completa = match.group(2)  # YYYYMMDD
        return fecha_completa[:6]        # Extraer YYYYMM
    return None

def extraer_fecha_completa(nombre_archivo):
    match = re.match(r"^(.*)_(\d{8})\.csv$", nombre_archivo)
    if match:
        return match.group(2)  # YYYYMMDD
    return None

def mover_a_error(archivo):
    if not os.path.exists(ERROR_FOLDER):
        os.makedirs(ERROR_FOLDER)
    
    origen = os.path.join(INPUT_FOLDER, archivo)
    destino = os.path.join(ERROR_FOLDER, archivo)
    shutil.move(origen, destino)
    logger.error(f"Archivo movido a carpeta de errores: {archivo}")

def procesar_archivo(archivo):
    try:
        ruta_archivo = os.path.join(INPUT_FOLDER, archivo)
        prefijo = extraer_prefijo(archivo)
        fecha_yyyymm = extraer_fecha_yyyymm(archivo)

        if not prefijo or prefijo not in ARCHIVO_TABLA_MAP:
            logger.warning(f"Archivo no reconocido o formato incorrecto: {archivo}")
            mover_a_error(archivo)
            return
        
        if not fecha_yyyymm:
            logger.warning(f"No se puede extraer la fecha del archivo: {archivo}")
            mover_a_error(archivo)
            return
        
        info = ARCHIVO_TABLA_MAP[prefijo]
        tabla = info["tabla"]
        tipo_insercion = info.get("tipo_insercion", "IGNORE")
        
        with open(ruta_archivo, newline = '', encoding='latin-1') as f:
            reader = csv.reader(f)
            encabezados_csv = next(reader)
            filas_originales = [row for row in reader]

        # Mapeo: encabezado CSV -> columna MySQL
        mapeo = info.get("mapeo_columnas", {})
        #fix para quitar espacios en blanco en cabeceras del csv
        encabezados_csv = [col.strip() for col in encabezados_csv]
        # Filtrar encabezados que sí están en el mapeo
        columnas_usadas_csv = [col for col in encabezados_csv if col in mapeo]
        # Obtener columnas reales de MySQL en orden correcto
        columnas_mysql = [mapeo[col] for col in columnas_usadas_csv]
        # Obtener columnas calculadas de ser necesario para tabla en mysql
        columnas_calculadas = info.get("columnas_calculadas", {})
        # Obtener índices de las columnas válidas en el CSV
        indices_usados = [encabezados_csv.index(col) for col in columnas_usadas_csv]

        # Reordenar y filtrar las filas con solo las columnas mapeadas
        filas_filtradas = [
            tuple(row[i] for i in indices_usados)
            for row in filas_originales
        ]

        filas_finales = []
        orden_columnas_calculadas = ordenar_columnas_calculadas(columnas_calculadas)

        columnas_csv_archivo = list(mapeo.values())
        columnas_extra = [col for col in orden_columnas_calculadas if col not in columnas_csv_archivo]
        columnas_finales = columnas_csv_archivo + columnas_extra #usadas para pasarlas como campos a insertar y no la cabecera del archivo
        todas_las_columnas = columnas_usadas_csv + columnas_extra #usadas para obtener los valores del archivo sin problema de mapeo

        for fila in filas_filtradas:
            fila_dict = dict(zip(columnas_usadas_csv, fila))
            fila_dict = incluir_columnas_calculadas(fila_dict, columnas_calculadas, orden_columnas_calculadas)
            
            fila_final = tuple(fila_dict.get(col) for col in todas_las_columnas)
            filas_finales.append(fila_final)

        # 🔄 Borrado previo si aplica  
        if not ejecutar_borrado_previo(info, filas_filtradas, columnas_usadas_csv, tabla, mover_a_error, archivo):
            return

        # ⬇️ Inserción
        insert_into_table(tabla, columnas_finales, filas_finales, batch_size=MAX_BATCH_SIZE, insert_type=tipo_insercion)
        logger.info(f"{len(filas_filtradas)} registros insertados en tabla '{tabla}' desde archivo: {archivo}")

        # ✅ Procedimientos
        try:
            ejecutar_procedimientos(info, fecha_yyyymm, mover_a_error_fn=mover_a_error, archivo=archivo)
        except Exception:
            return
        
        os.rename(ruta_archivo, os.path.join(PROCESSED_FOLDER, archivo))
        logger.info(f"Archivo procesado correctamente: {archivo}")
    
    except Exception as e:
        logger.error(f"Error procesando archivo {archivo}: {e}")
        logger.exception(e)
        mover_a_error(archivo)

