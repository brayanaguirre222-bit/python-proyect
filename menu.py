import gestor_reservas
import almacenamiento

def mostrar_matriz_disponibilidad(reservas):
    print("\n" + "="*85)
    print("                 MATRIZ DE DISPONIBILIDAD (09:00 a 23:00)")
    print("="*85)
    print(" Hora  | Libres | Estado de las mesas (15 max)           | Clientes Reservados")
    print("-" * 85)
    
    for hora in range(gestor_reservas.HORA_APERTURA, gestor_reservas.HORA_CIERRE):
        libres = gestor_reservas.calcular_mesas_disponibles_por_hora(reservas, hora)
        ocupadas = gestor_reservas.CAPACIDAD_TOTAL_MESAS - libres
        
        # Crear gráfico visual con cuadritos
        grafico = "■ " * ocupadas + "□ " * libres
        
        # Buscar los nombres de quienes reservaron en esta hora
        nombres_en_esta_hora = []
        for r in reservas:
            inicio = r.get('hora_inicio', 0)
            duracion = r.get('duracion', 0)
            fin = inicio + duracion
            
            # Si la hora actual está dentro del rango de la reserva del cliente
            if inicio <= hora < fin:
                # Agregamos el nombre y cuántas mesas ocupa para más claridad
                nombres_en_esta_hora.append(f"{r['nombre']} ({r.get('mesas_asignadas', 0)} mesas)")
                
        # Unir todos los nombres separados por coma
        texto_clientes = ", ".join(nombres_en_esta_hora)
        if not texto_clientes:
            texto_clientes = "-" # Muestra un guion si no hay reservas
            
        # Imprimir la fila completa ajustando los espacios (<30 alinea a la izquierda)
        print(f" {hora:02d}:00 |   {libres:02d}   | {grafico:<30} | {texto_clientes}")
        
    print("-" * 85)
    print("Leyenda: [□] Mesa libre   [■] Mesa ocupada\n")

def mostrar_menu():
    print("="*40)
    print("   SISTEMA DE RESERVAS - DON JOSÉ")
    print("="*40)
    print("1. Registrar nueva reserva")
    print("2. Buscar reserva")
    print("3. Ver matriz de disponibilidad")
    print("4. Cancelar (Eliminar) reserva")
    print("5. Salir")
    return input("Seleccione una opción: ")

def ejecutar():
    reservas_actuales = almacenamiento.cargar_reservas()

    while True:
        opcion = mostrar_menu()

        if opcion == "1":
            nombre = input("Nombre del responsable: ")
            try:
                personas = int(input("Cantidad de personas: "))
                hora_inicio = int(input("Hora de inicio (ej. 14 para las 2 de la tarde): "))
                duracion = int(input("Duración de la reserva en horas (ej. 2): "))
                
                exito, mensaje = gestor_reservas.validar_reserva(
                    nombre, personas, hora_inicio, duracion, reservas_actuales
                )
                
                if exito:
                    mesas_a_usar = gestor_reservas.calcular_mesas_necesarias(personas)
                    nueva_reserva = {
                        "nombre": nombre,
                        "personas": personas,
                        "mesas_asignadas": mesas_a_usar,
                        "hora_inicio": hora_inicio,
                        "duracion": duracion
                    }
                    reservas_actuales.append(nueva_reserva)
                    almacenamiento.guardar_reservas(reservas_actuales)
                    print(f"\n>> ÉXITO: Reserva creada. Se asignaron {mesas_a_usar} mesas de {hora_inicio}:00 a {hora_inicio+duracion}:00.\n")
                else:
                    print(f"\n>> {mensaje}\n")
            except ValueError:
                print("\n>> Error: Por favor ingrese solo números enteros para personas, hora y duración.\n")

        elif opcion == "2":
            nombre = input("Nombre a buscar: ")
            res = gestor_reservas.buscar_reserva(reservas_actuales, nombre)
            if res:
                print(f"\nReserva encontrada:\n - Cliente: {res['nombre']}\n - Personas: {res['personas']}\n - Mesas ocupadas: {res.get('mesas_asignadas', 0)}\n - Horario: de {res.get('hora_inicio', 0)}:00 a {res.get('hora_inicio', 0) + res.get('duracion', 0)}:00\n")
            else:
                print("\n>> No se encontró ninguna reserva con ese nombre.\n")

        elif opcion == "3":
            mostrar_matriz_disponibilidad(reservas_actuales)

        elif opcion == "4":
            nombre = input("Nombre de la reserva a eliminar: ")
            res = gestor_reservas.buscar_reserva(reservas_actuales, nombre)
            if res:
                reservas_actuales.remove(res)
                almacenamiento.guardar_reservas(reservas_actuales)
                print("\n>> Reserva eliminada. Mesas liberadas.\n")
            else:
                print("\n>> No se encontró la reserva.\n")

        elif opcion == "5":
            print("\nSaliendo del sistema... ¡Buen provecho en el restaurante, Don José!\n")
            break
        else:
            print("\n>> Opción no válida.\n")

if __name__ == "__main__":
    ejecutar()