import math

# Reglas del Negocio y Horarios
CAPACIDAD_TOTAL_MESAS = 15
ASIENTOS_POR_MESA = 10
HORA_APERTURA = 9
HORA_CIERRE = 23

def calcular_mesas_necesarias(cantidad_personas):
    """Calcula las mesas necesarias basándose en grupos de 10."""
    return math.ceil(cantidad_personas / ASIENTOS_POR_MESA)

def calcular_mesas_disponibles_por_hora(reservas, hora):
    """Calcula cuántas mesas hay libres en una hora específica (ej: a las 14:00)."""
    mesas_ocupadas = 0
    for r in reservas:
        inicio = r.get('hora_inicio', 0)
        duracion = r.get('duracion', 0)
        fin = inicio + duracion
        
        # Si la hora consultada está dentro del rango de la reserva, suma las mesas
        if inicio <= hora < fin:
            mesas_ocupadas += r.get('mesas_asignadas', 0)
            
    return CAPACIDAD_TOTAL_MESAS - mesas_ocupadas

def validar_reserva(nombre, cantidad_personas, hora_inicio, duracion, reservas):
    """Verifica que no se sobrepase el límite de mesas en ninguna de las horas solicitadas."""
    if not nombre.strip():
        return False, "Error: Toda reserva necesita un nombre."
    if cantidad_personas <= 0:
        return False, "Error: La cantidad de personas debe ser mayor a 0."
    if duracion <= 0:
        return False, "Error: La reserva debe durar al menos 1 hora."
        
    hora_fin = hora_inicio + duracion
    if hora_inicio < HORA_APERTURA or hora_fin > HORA_CIERRE:
        return False, f"Error: El horario es de {HORA_APERTURA}:00 a {HORA_CIERRE}:00. La reserva se sale del límite."

    mesas_requeridas = calcular_mesas_necesarias(cantidad_personas)
    
    # Comprobar la disponibilidad en cada hora que durará la reserva
    for hora in range(hora_inicio, hora_fin):
        libres = calcular_mesas_disponibles_por_hora(reservas, hora)
        if mesas_requeridas > libres:
            return False, f"Conflicto: Solo quedan {libres} mesas libres a las {hora}:00, y usted necesita {mesas_requeridas}."
            
    return True, ""

def buscar_reserva(reservas, nombre_cliente):
    for r in reservas:
        if r['nombre'].lower() == nombre_cliente.lower():
            return r
    return None