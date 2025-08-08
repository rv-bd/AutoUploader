from db import borrar_registros_por_valores
import logging

logger = logging.getLogger(__name__)

# ------------------------------------------------------
# 🧹 Borrar registros antes de insertar (si está configurado)
# ------------------------------------------------------
def ejecutar_borrado_previo(info, filas_filtradas, columnas_usadas_csv, tabla, mover_a_error_fn, archivo):
    borrar_config = info.get("borrar_antes_de_insertar")

    if not borrar_config:
        return True
    
    columna_csv = borrar_config.get("columna_csv")
    columna_mysql = borrar_config.get("columna_mysql")

    if columna_csv not in columnas_usadas_csv:
        logger.error(f"La columna '{columna_csv}' indicada para borrar no se encuentra en el archivo.")
        mover_a_error_fn(archivo)
        return False
    
    idx_csv = columnas_usadas_csv.index(columna_csv)

    valores_particion = set(
        row[idx_csv] for row in filas_filtradas
        if row[idx_csv] and row[idx_csv].strip() != ""
    )

    try:
        borrar_registros_por_valores(tabla, columna_mysql, valores_particion)
        return True
    except Exception:
        mover_a_error_fn(archivo)
        return False