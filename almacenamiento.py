import json
import os

# Esto obtiene la ruta exacta de la carpeta donde tienes este archivo de Python
CARPETA_ACTUAL = os.path.dirname(os.path.abspath(__file__))

# Esto une la ruta de tu carpeta con el nombre del archivo de texto
RUTA_ARCHIVO = os.path.join(CARPETA_ACTUAL, "datos_reservas.txt")

def guardar_reservas(reservas):
    """Guarda la lista de reservas en el archivo de texto plano (JSON)."""
    try:
        with open(RUTA_ARCHIVO, 'w', encoding='utf-8') as f:
            json.dump(reservas, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"\n[!] Error crítico al guardar los datos en el disco: {e}")

def cargar_reservas():
    """Carga las reservas antiguas apenas se abre el programa."""
    if not os.path.exists(RUTA_ARCHIVO):
        # Si el archivo no existe aún, devuelve una lista vacía
        return []
    try:
        with open(RUTA_ARCHIVO, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"\n[!] Error al intentar leer el archivo: {e}")
        return []