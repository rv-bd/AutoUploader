# 📁 Procesador de Archivos CSV a MySQL

Este proyecto en Python monitorea una carpeta de entrada, procesa archivos CSV dinámicos, los carga en tablas MySQL según configuración y ejecuta procedimientos almacenados. 

### 📦 Características:
- Carga automática de archivos CSV a MySQL
- Soporte de columnas mapeadas y calculadas
- Soporte para `INSERT`, `IGNORE`, y `REPLACE`
- Procedimientos almacenados posteriores a la carga
- Limpieza previa de datos (opcional)
- Logging y manejo de errores
- Cola de procesamiento para evitar sobrecarga
- Modular y extensible

---

## 📂 Estructura del Proyecto

project/
├── processor.py # Módulo principal
├── config.py # Configuración general
├── db.py # Funciones de conexión e inserción MySQL
├── logger.py # Logging
├── archivo_tabla_map.yaml # Configuración por archivo
├── run.bat # Script de ejecución en Windows (QUITADO)
├── logs/ # Guarda log diario
├── utils/ # Lógica modular
│ ├── init.py
│ ├── campos_dinamicos.py # Columnas calculadas
│ ├── pre_procesamiento.py # Lógica de borrado
│ └── post_procesamiento.py # Procedimientos almacenados
└── carpetas /
├── input/ # Carpeta de entrada (es dinamica y se configura en config.py)
├── processed/ # Archivos procesados (es dinamica y se configura en config.py)
└── error/ # Archivos con error (es dinamica y se configura en config.py)

---

## ⚙️ Requisitos

- Python 3.8+
- MySQL Server
- Pip packages: `pymysql`, `pyyaml`

Instala dependencias:
```bash
pip install -r requirements.txt

