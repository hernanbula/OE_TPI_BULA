##################################################################
# LIBRERIAS
import csv
from datetime import date, datetime
from pathlib import Path

##################################################################
# CONSTANTES
BASE_DIR = Path(__file__).resolve().parent
TURNOS_FILE = BASE_DIR / "turnos.csv"
TICKETS_FILE = BASE_DIR / "tickets.csv"

ESPECIALIDADES = {
    1: ("Clínica General", "CG"),
    2: ("Pediatría", "PD"),
    3: ("Traumatología", "TR"),
    4: ("Cardiología", "CA"),
    5: ("Neurología", "NE"),
    6: ("Dermatología", "DE"),
    7: ("Psicología", "PS"),
    8: ("ORL", "OR"),
    9: ("Otras consultas", "OC")
}

##################################################################
# FUNCIONES

def validar_dni():
    print("Para ser atendido debe ingresar su DNI.")
    while True:
        print("    " + "-" * 60)
        dni = input("    Ingrese (8 dígitos sin puntos ni espacios): ")
        try:
            dni_validado = int(dni)
            if dni_validado <= 999999:
                print("    ¡ERROR! El número del DNI ingresado es muy chico.\nIntente ingresarlo de nuevo.")
            elif dni_validado >= 99999999:
                print("    ¡ERROR! El número del DNI ingresado es muy grande.\nIntente ingresarlo de nuevo.")
            else:
                return str(dni_validado)
        except ValueError:
            print("    ¡ERROR! Eso no parece un número.\nIntente ingresarlo de nuevo.")


def leer_opcion_menu(min_opcion, max_opcion):
    while True:
        opcion = input(f"Seleccione opción ({min_opcion}-{max_opcion}): ")
        if opcion.isdigit():
            opcion = int(opcion)
            if min_opcion <= opcion <= max_opcion:
                return opcion
        print(f"ERROR: Debe ingresar un número entre {min_opcion} y {max_opcion}.")


def leer_opcion_si_no(prompt):
    while True:
        print(prompt)
        print("  1 - SÍ")
        print("  2 - NO")
        opcion = leer_opcion_menu(1, 2)
        return opcion == 1


def cargar_csv(file_path, headers):
    if not file_path.exists():
        with file_path.open("w", newline="", encoding="utf-8") as archivo:
            writer = csv.writer(archivo)
            writer.writerow(headers)
        return []

    with file_path.open("r", newline="", encoding="utf-8") as archivo:
        reader = csv.DictReader(archivo)
        return list(reader)


def cargar_turnos():
    return cargar_csv(TURNOS_FILE, ["dni", "apellido", "nombre", "especialidad", "fecha", "hora"])


def cargar_tickets():
    return cargar_csv(TICKETS_FILE, ["ticket", "dni", "especialidad", "obra_social", "fecha", "hora"])


def buscar_turno_por_dni(dni, turnos):
    for turno in turnos:
        if turno.get("dni") == dni:
            return turno
    return None


def seleccionar_especialidad():
    print("\nSeleccione una especialidad médica:")
    for numero, (nombre, codigo) in ESPECIALIDADES.items():
        print(f"  {numero}. {nombre} ({codigo})")
    opcion = leer_opcion_menu(1, len(ESPECIALIDADES))
    nombre, codigo = ESPECIALIDADES[opcion]
    print(f"Ha seleccionado: {nombre} ({codigo})")
    return codigo


def obtener_ultimo_numero(codigo_especialidad, tickets):
    ultimo_numero = 0
    for ticket in tickets:
        if ticket.get("especialidad") == codigo_especialidad:
            ticket_id = ticket.get("ticket", "")
            if "-" in ticket_id:
                partes = ticket_id.split("-", 1)
                if partes[0] == codigo_especialidad:
                    try:
                        ultimo_numero = max(ultimo_numero, int(partes[1]))
                    except ValueError:
                        pass
    return ultimo_numero


def generar_num_ticket(codigo_especialidad, tickets):
    siguiente_numero = obtener_ultimo_numero(codigo_especialidad, tickets) + 1
    return f"{codigo_especialidad}-{siguiente_numero:03d}"


def registrar_ticket(ticket, dni, especialidad, obra_social, fecha, hora):
    texto_obra_social = "SI" if obra_social else "NO"
    registro = [ticket, dni, especialidad, texto_obra_social, fecha, hora]
    escribir_encabezado = not TICKETS_FILE.exists() or TICKETS_FILE.stat().st_size == 0

    with TICKETS_FILE.open("a", newline="", encoding="utf-8") as archivo:
        writer = csv.writer(archivo)
        if escribir_encabezado:
            writer.writerow(["ticket", "dni", "especialidad", "obra_social", "fecha", "hora"])
        writer.writerow(registro)

    print("\nTicket registrado en el sistema.")


def imprimir_ticket(ticket, dni, especialidad, fecha, hora):
    print("\n======== TICKET DE ATENCIÓN ========")
    print(f"Número de ticket: {ticket}")
    print(f"Especialidad: {especialidad}")
    print(f"Fecha: {fecha}")
    print(f"Hora: {hora}")
    print(f"DNI: {dni}")
    print("Será llamado por la pantalla en la sala de espera.")
    print("===================================\n")


def procesar_paciente_sin_turno(dni):
    especialidad = seleccionar_especialidad()
    posee_obra_social = leer_opcion_si_no("\n¿Posee obra social?")

    if posee_obra_social:
        print("\nSe registró la atención como paciente con obra social.")
        print("Por favor, espere a ser llamado por recepción.")
        return

    tickets = cargar_tickets()
    ticket = generar_num_ticket(especialidad, tickets)
    fecha = date.today().isoformat()
    hora = datetime.now().strftime("%H:%M")
    registrar_ticket(ticket, dni, especialidad, posee_obra_social, fecha, hora)
    imprimir_ticket(ticket, dni, especialidad, fecha, hora)


def main():
    print("Bienvenido/a a Centro Médico Integral")
    tiene_turno = leer_opcion_si_no("¿Posee un turno previamente asignado?")
    dni = validar_dni()

    if tiene_turno:
        turnos = cargar_turnos()
        turno = buscar_turno_por_dni(dni, turnos)

        if turno is not None:
            print("\nTurno encontrado:")
            print(f"  DNI: {turno.get('dni')}")
            print(f"  Nombre: {turno.get('nombre', 'Desconocido')} {turno.get('apellido', '')}")
            print(f"  Especialidad: {turno.get('especialidad')}")
            print(f"  Fecha: {turno.get('fecha')}")
            print(f"  Hora: {turno.get('hora')}")
            return

        print(f"\nNo se encontró turno asociado al DNI {dni}.")
        print("El paciente continúa como paciente sin turno.")

    procesar_paciente_sin_turno(dni)


if __name__ == "__main__":
    main()
