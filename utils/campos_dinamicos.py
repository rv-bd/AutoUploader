from datetime import datetime, timedelta
from collections import defaultdict, deque
import logging

logger = logging.getLogger(__name__)

def convertir_fecha_formato(fecha_str, formato_fecha_columna, formato_fecha_salida, dias_a_restar = 0):
    fecha = datetime.strptime(fecha_str, formato_fecha_columna) - timedelta(days=dias_a_restar)
    return fecha.strftime(formato_fecha_salida)

def convertir_fecha(formato_fecha_salida, dias_a_restar = 0):
    fecha = datetime.now() - timedelta(days=dias_a_restar)
    return fecha.strftime(formato_fecha_salida)

def ordenar_columnas_calculadas(columnas_calculadas):
    grafo = defaultdict(list)
    grados_entrada = defaultdict(int)

    for campo, config in columnas_calculadas.items():
        depende = config.get("desde")
        dependiente = config.get("dependiente", False)

        if(depende and depende in columnas_calculadas and dependiente):
            grafo[depende].append(campo)
            grados_entrada[campo] += 1
        else:
            grados_entrada.setdefault(campo, 0)
    
    cola = deque([campo for campo, grado in grados_entrada.items() if grado == 0])
    orden = []

    while cola:
        actual = cola.popleft()
        orden.append(actual)

        for vecino in grafo[actual]:
            grados_entrada[vecino] -= 1

            if grados_entrada[vecino] == 0:
                cola.append(vecino)
    
    if len(orden) != len(columnas_calculadas):
        raise ValueError("Error: Hay una dependencia circular en columnas_calculadas")

    return orden

def incluir_columnas_calculadas(fila_dict, columnas_calculadas, orden_columnas):
    """
    Aplica las columnas calculadas en orden a un diccionario de fila original
    Devuelve fila_dict actualizado.
    """

    for nombre_col in orden_columnas:
        config = columnas_calculadas[nombre_col]
        tipo = config.get("tipo")

        if tipo == "fecha_desde_columna":
            nombre_origen = config.get("desde")
            formato_columna = config.get("formato_columna")
            formato_salida = config.get("formato_salida")
            dias_a_restar = config.get("dias_a_restar", 0)
            valor = fila_dict.get(nombre_origen)
    
            if valor:
                try:
                    valor_convertido = convertir_fecha_formato(valor, formato_columna, formato_salida, dias_a_restar=dias_a_restar)
                    fila_dict[nombre_col] = valor_convertido
                except Exception as e:
                    logger.exception(e)
                    fila_dict[nombre_col] = None
            else:
                fila_dict[nombre_col] = None
            
    
        elif tipo == "fecha_de_sistema":
            formato_fecha = config.get('formato_fecha')
            dias_a_restar = config.get('dias_a_restar', 0)
            
            fila_dict[nombre_col] = convertir_fecha(formato_fecha, dias_a_restar)
    
    return fila_dict