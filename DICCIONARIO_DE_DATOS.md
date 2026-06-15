# 📋 Diccionario de Datos - Sistema de Atención con Turnos

### UTN - TPaD - Organización Empresarial

### Trabajo Práctico Integrador: 
Gestión y emisión de tickets de atención mediante un turnero digital (chatbot) en Centro Médico Integral.

### Estudiante (Comisión N° 2): 
.  👤 BULA, Hernán Enrique, DNI 30.246.685

### Docentes:
#### .   👤 Coordinadora: Gabriela Martínez
#### .   👤 Profesora: Carolina Bruno
#### .   👤 Docente Tutora - Comisión 2: Mónica Mut
_
---
---

## 📊 Descripción General

Este documento detalla todas las variables, estructuras de datos y entidades manejadas por el sistema de chatbot para gestión de turnos médicos.

---

## 🗂️ ARCHIVOS CSV

### 📄 turnos.csv
**Propósito:** Almacena los turnos pre-asignados a pacientes.

| Campo | Tipo | Descripción | Ejemplo |
|-------|------|-------------|---------|
| `dni` | String (8 dígitos) | Número de identidad del paciente | `"30236685"` |
| `apellido` | String | Apellido del paciente | `"García"` |
| `nombre` | String | Nombre del paciente | `"Juan"` |
| `especialidad` | String | Nombre de la especialidad médica | `"Clínica General"` |
| `fecha` | String (YYYY-MM-DD) | Fecha del turno | `"2026-06-20"` |
| `hora` | String (HH:MM) | Hora del turno | `"14:30"` |

**Ejemplo de fila:**
```csv
dni,apellido,nombre,especialidad,fecha,hora
30236685,García,Juan,Clínica General,2026-06-20,14:30
```

---

### 📄 tickets.csv
**Propósito:** Registro de todos los números de atención generados en el sistema.

| Campo | Tipo | Descripción | Ejemplo |
|-------|------|-------------|---------|
| `ticket_id` | String | ID único del ticket (código + número correlativo) | `"CG002"` |
| `dni` | String (8 dígitos) | DNI del paciente atendido | `"30236685"` |
| `tiene_turno` | String (True/False) | Indica si el paciente tenía turno previo | `"True"` |
| `codigo_especialidad` | String (2 caracteres) | Código de la especialidad | `"CG"` |
| `obra_social` | String (True/False) | Si el paciente tiene cobertura | `"True"` |
| `fecha` | String (YYYY-MM-DD) | Fecha de emisión del ticket | `"2026-06-14"` |
| `hora` | String (HH:MM:SS) | Hora de emisión del ticket | `"16:58:45"` |

**Ejemplo de fila:**
```csv
ticket_id,dni,tiene_turno,codigo_especialidad,obra_social,fecha,hora
CG002,30236685,True,CG,True,2026-06-14,16:58:45
```

---

## 🔤 DICCIONARIO: ESPECIALIDADES

**Ubicación en código:** Constante `ESPECIALIDADES`

**Estructura:** Diccionario con clave numérica y valor tupla (nombre, código)

```python
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
```

| Opción | Nombre | Código |
|--------|--------|--------|
| 1 | Clínica General | CG |
| 2 | Pediatría | PD |
| 3 | Traumatología | TR |
| 4 | Cardiología | CA |
| 5 | Neurología | NE |
| 6 | Dermatología | DE |
| 7 | Psicología | PS |
| 8 | ORL | OR |
| 9 | Otras consultas | OC |

---

## 📦 VARIABLE GLOBAL: datos_solicitud

**Propósito:** Almacena temporalmente los datos de la solicitud del paciente durante una sesión.

**Estructura y tipos:**

```python
datos_solicitud = {
    "ticket_id": None,           # String: Ej. "CG002"
    "dni": None,                 # Integer: Ej. 30236685
    "tiene_turno": None,         # Boolean: True/False
    "apellido": None,            # String: Ej. "García"
    "nombre": None,              # String: Ej. "Juan"
    "especialidad": None,        # String: Código Ej. "CG"
    "obra_social": None,         # Boolean: True/False
    "fecha": None,               # String (YYYY-MM-DD): Ej. "2026-06-14"
    "hora": None                 # String (HH:MM): Ej. "16:58"
}
```

**Ciclo de vida:**
1. Se inicializa al comenzar cada sesión de usuario
2. Se rellena gradualmente según los estados FSM
3. Se vuelca a `tickets.csv` cuando se genera el ticket
4. Se reinicia después de FINALIZADO o CANCELANDO

---

## 🎭 MÁQUINA DE ESTADOS (FSM)

**Ubicación:** Enum `FSM_estado`

### Estados y transiciones:

```
┌─────────────────────────────────────────────────┐
│                    FLUJO FSM                     │
└─────────────────────────────────────────────────┘

INICIO
  ↓ [Enter]
ESPERANDO_DNI → valida DNI (8 dígitos)
  ↓
PREGUNTANDO_TURNO → ¿Tiene turno? [1=SÍ, 2=NO]
  ↓                    ↓                ↓
  └─ [1] ─────────────┤                └─ [2] ─→ ESPERANDO_ESPECIALIDAD
                      ↓
            VERIFICANDO_TURNO
                  ↓              ↓
           [Encontrado]    [No encontrado]
                ↓                  ↓
        (tiene_turno=True)   ESPERANDO_ESPECIALIDAD
                ↓
        PREGUNTANDO_COBERTURA
                ↓
        GENERANDO_TICKET
                ↓
        GUARDANDO_TICKET_LISTA → escribe en tickets.csv
                ↓
        IMPRIMIENDO_TICKET → muestra ticket en consola
                ↓
            FINALIZADO → reinicia datos → vuelve a INICIO

CANCELANDO (desde cualquier punto) → reinicia datos → INICIO

[ESC en INICIO] → salida del programa
```

| Estado | Descripción | Entrada del usuario |
|--------|-------------|-------------------|
| `INICIO` | Pantalla de bienvenida | Enter o ESC |
| `ESPERANDO_DNI` | Solicita validación de DNI | 8 dígitos numéricos |
| `PREGUNTANDO_TURNO` | Pregunta si tiene turno previo | 1 (SÍ), 2 (NO), 0 (CANCELAR) |
| `VERIFICANDO_TURNO` | Busca turno en turnos.csv | (automático) |
| `ESPERANDO_ESPECIALIDAD` | Muestra menú de especialidades | 0-9 |
| `PREGUNTANDO_COBERTURA` | Pregunta sobre obra social | 1 (SÍ), 2 (NO), 0 (CANCELAR) |
| `GENERANDO_TICKET` | Crea ID de ticket y registra fecha/hora | (automático) |
| `GUARDANDO_TICKET_LISTA` | Escribe en tickets.csv | (automático) |
| `IMPRIMIENDO_TICKET` | Muestra ticket formateado | (automático) |
| `FINALIZADO` | Mensaje de despedida y limpieza | (automático) |
| `CANCELANDO` | Cancela operación y vuelve a inicio | (automático) |

---

## 🎯 FLUJO DE DATOS POR ESCENARIO

### Escenario 1: Usuario CON turno previo (encontrado)

```
DNI ingresado → Búsqueda en turnos.csv → Turno encontrado
              ↓
        datos_solicitud["tiene_turno"] = True
        datos_solicitud["especialidad"] = turno.especialidad
        datos_solicitud["apellido"] = turno.apellido
        datos_solicitud["nombre"] = turno.nombre
              ↓
        Pregunta obra social → Genera ticket
```

### Escenario 2: Usuario CON turno previo (NO encontrado)

```
DNI ingresado → Búsqueda en turnos.csv → Turno NO encontrado
              ↓
        datos_solicitud["tiene_turno"] = False
              ↓
        Muestra menú de especialidades
              ↓
        Usuario elige especialidad → Genera ticket
```

### Escenario 3: Usuario SIN turno previo

```
Usuario responde "NO" a ¿Tiene turno?
              ↓
        datos_solicitud["tiene_turno"] = False
              ↓
        Muestra menú de especialidades
              ↓
        Usuario elige especialidad → Genera ticket
```

---

## 🔐 CONSTANTES DEL SISTEMA

| Constante | Valor | Descripción |
|-----------|-------|-------------|
| `BASE_DIR` | Path del directorio actual | Ubicación base para archivos CSV |
| `TURNOS_FILE` | BASE_DIR / "turnos.csv" | Ruta del archivo de turnos |
| `TICKETS_FILE` | BASE_DIR / "tickets.csv" | Ruta del archivo de tickets |

---

## 📝 VALIDACIONES DE DATOS

### DNI
- **Rango válido:** 1,000,000 a 99,999,999
- **Formato:** 8 dígitos sin puntos ni espacios
- **Tipo:** Entero (int)

### Opciones de menú
- **Rango válido:** Depende del menú específico
- **Tipo:** Entero (int)
- **Error:** Si no está en rango, se vuelve a solicitar

### Código de especialidad
- **Formato:** 2 caracteres alfabéticos
- **Validez:** Debe existir en diccionario `ESPECIALIDADES`

### Fecha y Hora
- **Fecha:** Formato ISO (YYYY-MM-DD)
- **Hora:** Formato HH:MM o HH:MM:SS
- **Origen:** Sistema operativo (date.today(), datetime.now())

---

## 🔄 SINCRONIZACIÓN ENTRE ARCHIVOS

```
turnos.csv (entrada)
    ↓
[Si usuario dice SÍ a "¿Tiene turno?"]
    ↓
buscar_turno_por_dni()
    ↓
Si encontrado → datos_solicitud se rellena desde turno.csv
Si NO encontrado → usuario ingresa datos manualmente
    ↓
tickets.csv (salida)
    ↓
registrar_ticket() escribe en tickets.csv
    ↓
tiene_turno = True/False según origen de datos
```

---

## 📊 EJEMPLO COMPLETO DE FLUJO

```
Usuario 1 (Con turno registrado):
  DNI: 30236685
  → Encontrado en turnos.csv
  → datos_solicitud["tiene_turno"] = True
  → datos_solicitud["especialidad"] = "Clínica General"
  → Pregunta obra social: SÍ
  → Ticket generado: CG002
  → Guardado en tickets.csv con tiene_turno="True"

Usuario 2 (Sin turno registrado):
  DNI: 23456789
  → NO encontrado en turnos.csv
  → datos_solicitud["tiene_turno"] = False
  → Usuario elige especialidad: Pediatría (PD)
  → Pregunta obra social: NO
  → Ticket generado: PD001
  → Guardado en tickets.csv con tiene_turno="False"
```

---

## 🛠️ MANTENIMIENTO DE DATOS

### Limpiar datos entre sesiones
La función `reiniciar_datos()` resetea `datos_solicitud` después de cada usuario:
```python
def reiniciar_datos():
    global datos_solicitud
    datos_solicitud = { ... }  # todos los valores a None
```

### Generar archivos CSV nuevos
Si los archivos no existen, `cargar_csv()` los crea automáticamente con los headers correctos.

### Actualizar especialidades
Modificar el diccionario `ESPECIALIDADES` automáticamente actualiza:
- El menú mostrado al usuario
- Los códigos disponibles para tickets
- La búsqueda en turnos.csv

---

**Documento generado con asistencia de GitHub Copilot**
```