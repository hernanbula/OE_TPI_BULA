##################################################################
# # LIBRERIAS
import csv
from datetime import date, datetime
from pathlib import Path
import sys
import tty
import termios

# Mejoras visuales generadas con ayuda de GitHub Copilot
# Importaciones de la librería RICH para mejorar la interfaz visual
# RICH es una librería que permite crear interfaces CLI profesionales con colores, tablas, paneles, etc.
from rich.console import Console  # Consola mejorada con soporte para colores y estilos
from rich.table import Table  # Componente para crear tablas formateadas
from rich.panel import Panel  # Componente para crear paneles con bordes decorativos
from rich.align import Align  # Para alinear contenido
from rich.text import Text  # Para texto con estilos personalizados
from rich.rule import Rule  # Para crear líneas divisoras con texto

# Inicializar consola con soporte para colores ANSI
# Esta instancia 'console' se usará en todo el código para imprimir con estilos
console = Console()

##################################################################
# CONSTANTES 
# Generado con asistencia de GitHub Copilot
# Son constantes para guardar la ubicación de los archivos de datos del chatbot, 
# y se calculan a partir de dónde está el código que se ejecuta, 
# para que funcione sin importar dónde se ejecute el programa.
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
    9: ("Otras consultas", "OC"),
}

##################################################################
# MAQUINA DE ESTADOS - FSM

from enum import Enum

class FSM_estado(Enum):
    INICIO = "inicio"
    ESPERANDO_DNI = "esperando_dni"
    PREGUNTANDO_TURNO = "preguntando_turno"
    VERIFICANDO_TURNO = "verificando_turno"
    ESPERANDO_ESPECIALIDAD = "esperando_especialidad"
    PREGUNTANDO_COBERTURA = "preguntando_cobertura"
    GENERANDO_TICKET = "generando_ticket"
    GUARDANDO_TICKET_LISTA = "guardando_ticket_lista"
    IMPRIMIENDO_TICKET = "imprimiendo_ticket"
    FINALIZADO = "finalizado"
    CANCELANDO = "cancelando"

# Almacena el estado actual y los datos temporales para cada usuario
estado_actual = FSM_estado.INICIO
global datos_solicitud
datos_solicitud = {
    "ticket_id": None,
    "dni": None,
    "tiene_turno": None,
    "apellido": None,
    "nombre": None,
    "especialidad": None,
    "obra_social": None,
    "fecha": None,
    "hora": None
}

##################################################################
# FUNCIONES

# Función para leer una única tecla sin esperar Enter, con asistencia de GitHub Copilot
def leer_tecla_una():
    """Lee una única tecla sin esperar Enter. Devuelve el carácter (ESC = '\\x1b')."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

# Funcion validar DNI
# Mejoras visuales con asistencia de GitHub Copilot: Usa Panel para crear un recuadro, colores para mensajes
def validar_dni():
    console.print(Panel("🆔 Validación de DNI", style="bold blue", expand=False))  # Panel() crea un recuadro decorativo con borde  # style="bold blue" aplica color azul y negrita al panel # expand=False hace que el panel se ajuste al contenido
    console.print("Para ser atendido debe ingresar su DNI.")
    while True:
        console.print("─" * 60)  # Línea divisoria
        dni = input("    Ingrese (8 dígitos sin puntos ni espacios): ") # Pide la respuesta del usuario
        try:
            dni_validado = int(dni) # Intentamos convertir la entrada a un entero
            if dni_validado <= 999999:
                console.print("    [red]✗ ERROR[/red] El número del DNI ingresado es muy chico.\n    Intente ingresarlo de nuevo.")
            elif dni_validado >= 99999999: # Valida que esté en el rango
                console.print("    [red]✗ ERROR[/red] El número del DNI ingresado es muy grande.\n    Intente ingresarlo de nuevo.") 
            else: 
                console.print(f"    [green]✓ DNI válido: {dni_validado}[/green]")
                return dni_validado
        except ValueError: # Si int() falla, Python lanza un ValueError
            console.print("    [red]✗ ERROR[/red] Eso no parece un número.\n    Intenta ingresarlo de nuevo.") # Da error si se ingresan caracteres no numéricos


# Función para solicitar al usuario la opción de menu entre un rango de numeros
def leer_opcion_menu(min_opcion, max_opcion):
    while True:
        opcion = input(f"→ Seleccione opción ({min_opcion}-{max_opcion}): ")
        if opcion.isdigit():
            opcion = int(opcion)
            if min_opcion <= opcion and opcion <= max_opcion:
                return opcion
        console.print(f"[red]✗ ERROR:[/red] Debe ingresar un número entre {min_opcion} y {max_opcion}")


# Función para leer opción: Si o No (S/N)
def leer_opcion_si_no_cancelar(prompt):
    while True:
        console.print(f"\n{prompt}")
        console.print("  [green]1 - SÍ[/green]") # [green] para color verde que indica éxito/confirmación
        console.print("  [yellow]2 - NO[/yellow]") # [yellow] y [/yellow] son tags de rich para aplicar color amarillo
        console.print("  [red]0 - CANCELAR Y VOLVER AL INICIO[/red]") # [red] y [/red] son tags de rich para aplicar color rojo
        opcion = leer_opcion_menu(0, 2)
        if opcion == 1:
            return 1 
        elif opcion == 2:
            return 2
        elif opcion == 0:
            return 0
        else:
            console.print("[red]✗ ERROR:[/red] Debe ingresar 1 para SÍ, 2 para NO o 0 para CANCELAR.")


# Función para cargar un archivo CSV y devolver su contenido como una lista de listas
# Generado con asistencia de GitHub Copilot
# Si el archivo no existe, se crea uno nuevo con los encabezados especificados
def cargar_csv(file_path, headers):
    """Lee un CSV y devuelve una lista de diccionarios usando los encabezados.

    Si el archivo no existe, lo crea con los `headers` proporcionados y devuelve una lista vacía.
    `file_path` puede ser una ruta (str) o un objeto `Path`.
    """
    path = Path(file_path)
    if not path.exists():
        print(f"Archivo {path} no encontrado. Se creará uno nuevo.")
        with path.open(mode='w', newline='', encoding='utf-8') as archivo:
            writer = csv.writer(archivo)
            writer.writerow(headers)
        return []

    with path.open('r', newline='', encoding='utf-8') as archivo:
        reader = csv.DictReader(archivo)
        return list(reader)


# Función para cargar turnos desde archivo CSV, con asistencia de GitHub Copilot
# Utilizando la función cargar_csv para leer el contenido del archivo y devolverlo como una lista de listas.
def cargar_turnos(): 
    return cargar_csv(TURNOS_FILE, ["dni", "apellido", "nombre", "especialidad", "fecha", "hora"])


# Función para cargar tickets desde archivo CSV
# Utilizando la función cargar_csv para leer el contenido del archivo y devolverlo como una lista de listas.
def cargar_tickets(): 
    return cargar_csv(TICKETS_FILE, ["ticket_id", "dni", "tiene_turno", "codigo_especialidad", "obra_social", "fecha", "hora"])


# Función para buscar un turno por DNI  
def buscar_turno_por_dni(dni, turnos):
    for turno in turnos:
        if turno.get("dni") == str(dni):
            return turno
    return None


# Función para ver opciones de un menú:
# Mejoras visuales generadas con asistencia de GitHub Copilot: Usa Table para crear tablas formateadas con estilos
def opciones_especialidades():
    console.print()
    console.print(Panel("🏥 ESPECIALIDADES MÉDICAS DISPONIBLES", style="bold blue", expand=False))
    
    # Table() es un componente de rich que crea tablas formateadas
    # show_header=True muestra la fila de encabezados
    # header_style="blue" aplica color azul a los encabezados
    # padding=(0, 1) define espacios alrededor del contenido de cada celda
    table = Table(show_header=True, header_style="blue", padding=(0, 1))
    
    # add_column() agrega columnas a la tabla
    # style="dim" hace que el texto sea más oscuro/atenuado
    table.add_column("Opción", style="dim")
    table.add_column("Especialidad", style="white")
    table.add_column("Código", style="dim")
    
    # Llenar la tabla con datos del diccionario ESPECIALIDADES
    for clave, (nombre, codigo) in ESPECIALIDADES.items():
        table.add_row(str(clave), nombre, codigo)
    
    table.add_row("0", "Salir de la aplicación", "─")
    console.print(table)
    console.print("─" * 65)  # Línea divisoria
    console.print("Elija una especialidad médica para ser atendido:")
    return leer_opcion_menu(0, max(ESPECIALIDADES))

# FUnción para elegir especialidad médica
def seleccionar_especialidad(opcion):
    if opcion == 0:
        return 0

    especialidad = ESPECIALIDADES.get(opcion)

    if especialidad is None:
        console.print("[red]✗ Opción de especialidad inválida.[/red]")
        return None

    nombre, codigo = especialidad
    console.print(f"\n[green]✓ Usted eligió:[/green] {nombre}\n")
    return codigo

# Funcion obra social
def preguntar_obra_social():
    obra_social = leer_opcion_si_no_cancelar("¿Posee obra social?")
    if obra_social == 1:
        return True
    elif obra_social == 2:
        return False
    elif obra_social == 0:
        return 0
    
# Obtener último número de especialidad en ticket.csv
# Realizado con ayuda de GitHub Copilot
def obtener_ultimo_numero(codigo_especialidad):
    if not TICKETS_FILE.exists():
        return 0

    with TICKETS_FILE.open(mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)  # salta el encabezado si existe
        ultimo_numero = 0  # Si no encuentra ningún ticket para esa especialidad, devuelve 0
        for row in reader:
            if len(row) < 7:  # Verifica que la fila tenga al menos 7 columnas para evitar errores de índice
                continue
            if row[3] == codigo_especialidad:  # si el código de especialidad coincide
                try:
                    numero = int(row[0][2:])  # obtiene el número del ticket (sin el código de especialidad)
                except (ValueError, IndexError):
                    continue
                if numero > ultimo_numero:  # si el número es mayor que el último número encontrado, lo actualiza
                    ultimo_numero = numero
    return ultimo_numero

# Generar numero de ticket
def generar_ticket_id(codigo_especialidad):
    ticket_id = f"{codigo_especialidad}{obtener_ultimo_numero(codigo_especialidad)+1:03d}"
    return ticket_id

# Función para registrar ticket en tickets.csv
def registrar_ticket(ticket_id, dni, tiene_turno, codigo_especialidad, obra_social, fecha, hora):
    modo = 'a' if TICKETS_FILE.exists() else 'w'
    with TICKETS_FILE.open(mode=modo, newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if modo == 'w':
            writer.writerow(["ticket_id", "dni", "tiene_turno", "codigo_especialidad", "obra_social", "fecha", "hora"])
        writer.writerow([ticket_id, dni, "True" if tiene_turno else "False", codigo_especialidad, obra_social, fecha, hora])
    console.print("[green]✓ Ticket registrado correctamente[/green]")

# Función para mostrar turno encontrado
# Mejoras visuales generadas con asistencia de GitHub Copilot: Tabla dentro de un Panel
def mostrar_turno(turno):
    if turno is None:
        console.print("\n[red]✗ No se encontró un turno registrado con ese DNI.[/red]\n")
        return False
    
    # Crear tabla para mostrar el turno de forma organizada
    # show_header=False porque solo hay dos columnas (Campo-Valor)
    table = Table(show_header=False, padding=(0, 2))
    table.add_column("Campo", style="blue")  # Nombre de los campos en azul
    table.add_column("Valor", style="white")  # Valores en blanco
    
    # Agregar filas con la información del turno
    table.add_row("DNI", turno.get('dni', 'N/A'))
    table.add_row("Nombre", f"{turno.get('nombre', 'Desconocido')} {turno.get('apellido', '')}")
    table.add_row("Especialidad", turno.get('especialidad', 'N/A'))
    table.add_row("Fecha", turno.get('fecha', 'N/A'))
    table.add_row("Hora", turno.get('hora', 'N/A'))
    
    console.print()
    console.print(Panel(
        table,
        title="[blue]📄 Turno Encontrado[/blue]",
        style="blue",
        expand=False
    ))
    return True

# Función para imprimir ticket
def imprimir_ticket(ticket_id, dni, tiene_turno, codigo_especialidad, obra_social, fecha, hora):
    # Buscar nombre de especialidad por código
    especialidad_nombre = None
    for clave, (nombre, codigo) in ESPECIALIDADES.items():
        if codigo == codigo_especialidad:
            especialidad_nombre = nombre
            break
    
    # Crear ticket con diseño profesional usando caracteres Unicode para bordes
    # Caracteres utilizados:
    #   ┌ ─ ┐  : esquina superior
    #   │    : lado vertical
    #   ├ ─ ┤  : línea divisoria intermedia
    #   └ ─ ┘  : esquina inferior
    # {:^58} centra el texto en 58 caracteres de ancho
    # {" " * 58} crea espacios en blanco para separación visual
    # Mejoras visuales generadas con asistencia de GitHub Copilot: 
    # Formato ASCII art con caracteres Unicode para crear un ticket profesional

    ticket_text = f"""
┌{"─" * 58}┐
│ {" " * 58}│
│ {'CENTRO MÉDICO INTEGRAL':^58}│
│ {'Número de Atención':^58}│
│ {" " * 58}│
│ {ticket_id:^58}│
│ {" " * 58}│
├{"─" * 58}┤
│ {f"Especialidad: {especialidad_nombre}":58}│
│ {f"DNI del paciente: {dni}":58}│
│ {f"Con turno: {'Sí' if tiene_turno else 'No'}":58}│
│ {f"Obra Social: {'Con cobertura' if obra_social == 'True' or obra_social == True else 'Sin cobertura'}":58}│
│ {f"Fecha: {fecha}":58}│
│ {f"Hora: {hora}":58}│
│ {" " * 58}│
└{"─" * 58}┘
    """
    
    console.print(ticket_text, style="blue")
    console.print(Panel(
        "[green]✓ Será llamado por la pantalla en la sala de espera[/green]",
        style="green",
        expand=False
    ))
    console.print("\n[dim]⚠ Guarde este número para referencia[/dim]\n")

# Funcion para reiniciar los datos de la solicitud después de finalizar o cancelar una atención, 
# para que no persistan datos incompletos y que el siguiente usuario comience con datos limpios
def reiniciar_datos():
    global datos_solicitud
    datos_solicitud = {
        "ticket_id": None,
        "dni": None,
        "tiene_turno": None,
        "apellido": None,
        "nombre": None,
        "especialidad": None,
        "obra_social": None,
        "fecha": None,
        "hora": None
    }

##################################################################
# MAIN
##################################################################
# Programa principal 
# 
# Mejoras visuales generadas con asistencia de GitHub Copilot

# Pantalla de bienvenida. # Panel() crea un recuadro decorativo con contenido personalizado

##################################
# MAQUINA DE ESTADOS - FSM

programa_activo = True

while programa_activo:
    if estado_actual == FSM_estado.INICIO:
        console.print(Panel(
        "🏥 CENTRO MÉDICO INTEGRAL 🏥\nSistema de Atención con Turnos",
        style="bold blue", expand=False))
        console.print("[dim]Presione Enter para continuar o ESC para salir.[/dim]")
        # Leer una tecla. Generado con asistencia de GitHub Copilot.
        # Si es ESC, salir del programa. Si es Enter, continuar normalmente.
        tecla = leer_tecla_una()
        if tecla == '\x1b':  # ESC
            console.print(Panel(
            "🏥 CENTRO MÉDICO INTEGRAL 🏥\nUsted salió del Sistema de Atención con Turnos",
            style="red", expand=False))
            programa_activo = False
            break
        # Si presionó cualquier otra tecla (p. ej. Enter), continuar normalmente
        estado_actual = FSM_estado.ESPERANDO_DNI
    
    elif estado_actual == FSM_estado.ESPERANDO_DNI:
    # Validar DNI
        datos_solicitud["dni"] = validar_dni()
        estado_actual = FSM_estado.PREGUNTANDO_TURNO

    elif estado_actual == FSM_estado.PREGUNTANDO_TURNO:
        # Preguntar si tiene turno
        datos_solicitud["tiene_turno"] = leer_opcion_si_no_cancelar("❓ ¿Tiene un turno previamente asignado?")
        if datos_solicitud["tiene_turno"] == 0: # Si el usuario elige cancelar, vuelve al inicio
            estado_actual = FSM_estado.CANCELANDO
        else:
            estado_actual = FSM_estado.VERIFICANDO_TURNO

    elif estado_actual == FSM_estado.VERIFICANDO_TURNO:
        # Si tiene turno, entonces buscar por DNI en turnos.csv y mostrar el turno encontrado. 
        if datos_solicitud["tiene_turno"] == 1:
            turnos = cargar_turnos()
            turno = buscar_turno_por_dni(datos_solicitud["dni"], turnos) # buscar por DNI
            datos_solicitud["turno"] = turno
            if mostrar_turno(turno): # Si se encontró el turno
                datos_solicitud["tiene_turno"] = True
                datos_solicitud["especialidad"] = turno.get('especialidad')
                estado_actual = FSM_estado.PREGUNTANDO_COBERTURA
            else: # Si no se encontró el turno, se le informa al usuario y se le pregunta por la especialidad que desea ser atendido.
                console.print("[dim]No se encontró el turno asociado a su DNI.[/dim]\n")
                console.print("[dim]Le asignaremos un número de atención sin turno.[/dim]\n")
                datos_solicitud["tiene_turno"] = False
                estado_actual = FSM_estado.ESPERANDO_ESPECIALIDAD    
        else: # Si el usuario dice que no tiene turno, se salta la verificación y va directo a elegir especialidad
            console.print("[dim]Le asignaremos un número de atención sin turno.[/dim]\n")
            datos_solicitud["tiene_turno"] = False
            estado_actual = FSM_estado.ESPERANDO_ESPECIALIDAD


    elif estado_actual == FSM_estado.ESPERANDO_ESPECIALIDAD:
        # Si tiene turno y se encontró el turno, cargar la especialidad del turno encontrado. 
        if datos_solicitud["tiene_turno"]:
            datos_solicitud["especialidad"] = datos_solicitud["turno"].get('especialidad')
            console.print(f"Trabajando con su especialidad registrada: {datos_solicitud['especialidad']}\n")
            estado_actual = FSM_estado.PREGUNTANDO_COBERTURA
        # Si el usuario no tiene turno o no se encontró el turno registrado, 
        # entonces se le pregunta por la especialidad que desea ser atendido.
        else:
            datos_solicitud["especialidad"] = seleccionar_especialidad(opciones_especialidades())

            if datos_solicitud["especialidad"] == 0: # Si el usuario elige cancelar, se cambia el estado a CANCELANDO para que el programa termine
                estado_actual = FSM_estado.CANCELANDO
            else:
                estado_actual = FSM_estado.PREGUNTANDO_COBERTURA

    elif estado_actual == FSM_estado.PREGUNTANDO_COBERTURA:
        # Preguntar obra social
        datos_solicitud["obra_social"] = preguntar_obra_social()
        if datos_solicitud["obra_social"] == 0:
            estado_actual = FSM_estado.CANCELANDO
        else:
            estado_actual = FSM_estado.GENERANDO_TICKET

    elif estado_actual == FSM_estado.GENERANDO_TICKET:
        # Registrar fecha y hora del ticket
        datos_solicitud["fecha"] = date.today().isoformat()
        datos_solicitud["hora"] = datetime.now().isoformat()

        # Generar número de ticket correlativo para la especialidad
        datos_solicitud["ticket_id"] = generar_ticket_id(datos_solicitud["especialidad"])
        estado_actual = FSM_estado.GUARDANDO_TICKET_LISTA

    elif estado_actual == FSM_estado.GUARDANDO_TICKET_LISTA:
        # Registrar ticket
        registrar_ticket(datos_solicitud["ticket_id"], datos_solicitud["dni"], datos_solicitud["tiene_turno"], datos_solicitud["especialidad"], datos_solicitud["obra_social"], datos_solicitud["fecha"], datos_solicitud["hora"])
        estado_actual = FSM_estado.IMPRIMIENDO_TICKET

    elif estado_actual == FSM_estado.IMPRIMIENDO_TICKET:
        # Mostrar banner de espera con Rule (línea divisoria con texto)
        # Rule() es un componente de rich que crea una línea decorativa con texto en el medio
        # style="blue" aplica color azul a la línea
        console.print()
        console.print(Rule("Generando su número de atención", style="blue"))
        console.print()

        # Cambia el formato de fecha al español:
        datos_solicitud["fecha"] = date.today().strftime("%d/%m/%Y")
        # Usa %H:%M:%S si quieres incluir segundos
        datos_solicitud["hora"] = datetime.now().strftime("%H:%M")

        # Imprimir ticket formateado
        imprimir_ticket(datos_solicitud["ticket_id"], datos_solicitud["dni"], datos_solicitud["tiene_turno"], datos_solicitud["especialidad"], datos_solicitud["obra_social"], datos_solicitud["fecha"], datos_solicitud["hora"])
        estado_actual = FSM_estado.FINALIZADO
    
    elif estado_actual == FSM_estado.FINALIZADO:
        print("=" * 60) # Separador visual entre solicitudes")
        print("=" * 60) # Separador visual entre solicitudes")
        console.print("[green]Gracias por usar el sistema. ¡Hasta luego![/green]")
        print("=" * 60) # Separador visual entre solicitudes")
        reiniciar_datos()
        estado_actual = FSM_estado.INICIO

    elif estado_actual == FSM_estado.CANCELANDO:
        print("=" * 60) # Separador visual entre solicitudes")
        print("=" * 60) # Separador visual entre solicitudes")
        console.print(Panel("[red]Proceso cancelado. Volviendo al inicio...[/red]", style="red", expand=False))
        print("=" * 60) # Separador visual entre solicitudes")
        print("=" * 60) # Separador visual entre solicitudes")
        reiniciar_datos()
        estado_actual = FSM_estado.INICIO