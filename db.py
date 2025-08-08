import mysql.connector
from config import DB_CONFIG, DB_CONFIG_LOCAL
from logger import configurar_logger

logger = configurar_logger()

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def insert_into_table(table_name, columns, values, batch_size=5000, insert_type = "INSERT"):
    conn = get_connection()
    cursor = conn.cursor()

    insert_type = insert_type.upper()
    if insert_type not in ("INSERT", "IGNORE", "REPLACE"):
        raise ValueError(f"Tipo de insercion no valido: {insert_type}")

    if insert_type == "IGNORE":
        comando_sql = "INSERT IGNORE INTO"
    elif insert_type == "REPLACE":
        comando_sql = "REPLACE INTO"
    else:
        comando_sql = "INSERT INTO"

    placeholders = ','.join(['%s'] * len(columns))
    columns_str = ','.join(columns)
    sql = f"{comando_sql} {table_name} ({columns_str}) VALUES ({placeholders})"
    
    total_rows = len(values)
    for i in range(0, total_rows, batch_size):
        batch = values[i:i+batch_size]
        try:
            cursor.executemany(sql, batch)
            conn.commit()
        except Exception as e:
            logger.exception(e)
            conn.rollback()
            raise e

    cursor.close()
    conn.close()

def execute_stored_procedure(procedure_name, args=None):
    conn = get_connection()
    cursor = conn.cursor()

    if args:
        cursor.callproc(procedure_name, args)
    else:
        cursor.callproc(procedure_name)
    
    conn.commit()
    cursor.close()
    conn.close()

def borrar_registros_por_valores(tabla, columna_mysql, valores):
    """
    Elimina registros de una tabla donde columna_mysql = cada valor en la lista.
    """
    if not valores:
        return  # No hay nada que borrar

    try:
        conn = get_connection()
        cursor = conn.cursor()

        for valor in valores:
            logger.info(f"Borrando de '{tabla}' donde {columna_mysql} = {valor}")
            sql = f"DELETE FROM {tabla} WHERE {columna_mysql} = %s"
            cursor.execute(sql, (valor,))

        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        logger.error(f"Error al borrar registros en '{tabla}': {e}")
        raise