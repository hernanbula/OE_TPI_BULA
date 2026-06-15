# Código generado con ayuda de DeepSeek y GitHub Copilot
# Este script genera un archivo CSV con turnos y tickets aleatorios para una clínica, 
# incluyendo campos como DNI, apellido, nombre, especialidad, obra social, fecha y hora de atención.

import csv
import random
from datetime import datetime, timedelta
import os

# Configuración
CANTIDAD_TURNOS = 50  # Cambia esta cantidad según necesites
DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_TURNOS = os.path.join(DIRECTORIO_ACTUAL, "turnos.csv")
ARCHIVO_TICKETS = os.path.join(DIRECTORIO_ACTUAL, "tickets.csv")

# Especialidades: (nombre, codigo)
ESPECIALIDADES = [
    ("Clinica General", "CG"),
    ("Pediatria", "PD"),
    ("Traumatologia", "TR"),
    ("Cardiologia", "CA"),
    ("Neurologia", "NE"),
    ("Dermatologia", "DE"),
    ("Psicologia", "PS"),
    ("ORL", "OR"),
    ("Otras consultas", "OC"),
]

# Listas de nombres y apellidos
APELLIDOS = [
    "Garcia", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Perez",
    "Sanchez", "Ramirez", "Torres", "Flores", "Rivera", "Cruz", "Moreno", "Gutierrez",
    "Ortiz", "Jimenez", "Vargas", "Castro", "Silva", "Rojas", "Molina", "Ramos",
    "Medina", "Reyes", "Ruiz", "Soto", "Delgado", "Campos", "Romero", "Bula"
]

NOMBRES = [
    "Juan", "Maria", "Carlos", "Ana", "Pedro", "Rosa", "Miguel", "Lucia", "Jose",
    "Carmen", "Fernando", "Isabel", "Antonio", "Francisca", "Manuel", "Elena",
    "Rafael", "Esperanza", "Diego", "Gloria", "Jorge", "Laura", "Andres", "Catalina",
    "Ramon", "Beatriz", "Hernan", "Susana", "Gabriel", "Magdalena"
]

# Probabilidad de tener obra social (70% True, 30% False)
PROB_OBRA_SOCIAL = 0.7

# Probabilidad de tener turno (70% True, 30% False)
PROB_TURNO = 0.7

# Rango de fechas (entre el 1 y el 30 de junio de 2026)
FECHA_INICIO = datetime(2026, 6, 1)
FECHA_FIN = datetime(2026, 6, 30)

# Rango de horas (entre 8:00 y 18:00)
HORA_INICIO = 8
HORA_FIN = 18

# Función para generar DNI aleatorio (7 u 8 dígitos)
def generar_dni():
    return random.randint(1000000, 99999999)

# Funcion generar nombres y apellidos aleatorios
def generar_nombres_apellidos():
    nombre = random.choice(NOMBRES)
    apellido = random.choice(APELLIDOS)
    return apellido, nombre

# Función para generar fecha y hora aleatoria
def generar_fecha_hora():
    dias_diferencia = (FECHA_FIN - FECHA_INICIO).days
    dias_aleatorios = random.randint(0, dias_diferencia)
    fecha = FECHA_INICIO + timedelta(days=dias_aleatorios)
    hora = random.randint(HORA_INICIO, HORA_FIN - 1)
    minuto = random.randint(0, 59)
    segundo = random.randint(0, 59)
    fecha_hora = fecha.replace(hour=hora, minute=minuto, second=segundo)
    return fecha_hora.strftime("%Y-%m-%d"), fecha_hora.strftime("%H:%M:%S")

# Generar turnos y tickets
# Primero, crear un diccionario para llevar el último número por especialidad
contadores = {codigo: 0 for _, codigo in ESPECIALIDADES}
turnos = []
tickets = []

for _ in range(CANTIDAD_TURNOS):
    # Elegir especialidad aleatoria
    especialidad_nombre, codigo = random.choice(ESPECIALIDADES)
    # Incrementar contador para esa especialidad
    contadores[codigo] += 1
    numero_ticket = contadores[codigo]
    ticket_id = f"{codigo}{numero_ticket:03d}"
    apellido, nombre = generar_nombres_apellidos()
    dni = generar_dni()
    obra_social = True if random.random() < PROB_OBRA_SOCIAL else False
    tiene_turno = True if random.random() < PROB_TURNO else False
    fecha, hora = generar_fecha_hora()

    turnos.append([dni, apellido, nombre, codigo, obra_social, fecha, hora])    
    tickets.append([ticket_id, dni, tiene_turno, codigo, obra_social, fecha, hora])

# Escribir archivos CSV
with open(ARCHIVO_TICKETS, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["ticket_id", "dni", "tiene_turno", "codigo_especialidad", "obra_social", "fecha", "hora"])
    writer.writerows(tickets)

# Escribir archivo CSV
with open(ARCHIVO_TURNOS, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["dni", "apellido", "nombre", "codigo_especialidad", "obra_social", "fecha", "hora"])
    writer.writerows(turnos)

print(f"Se generaron {CANTIDAD_TURNOS} turnos en {ARCHIVO_TURNOS}")
print(f"Se generaron {CANTIDAD_TURNOS} tickets en {ARCHIVO_TICKETS}")
