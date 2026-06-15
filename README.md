# README
## Chatbot: Sistema de Atención con Turnos

### UTN - TPaD - Organización Empresarial

### Trabajo Práctico Integrador: 
Gestión y emisión de tickets de atención mediante un turnero digital (chatbot) en Centro Médico Integral.

### Estudiante (Comisión N° 2): 
.  👤 BULA, Hernán Enrique, DNI 30.246.685

### Docentes:
#### .   👤 Coordinadora: Gabriela Martínez
#### .   👤 Profesora: Carolina Bruno
#### .   👤 Docente Tutora - Comisión 2: Mónica Mut

---

##  ℹ️ Descripción General

Sistema interactivo de chatbot para gestión de turnos médicos en un centro de salud. El programa permite a los pacientes ingresar solicitudes de atención, verifica turnos previos y genera tickets de espera con código de especialidad.

---
## 📄 Archivos txt y diagramas BPMN

| Archivo | Descripción |
|---------|-------------|
| **[TPI_OE_BULA_Comision2](./txt/TPI_OE_BULA_Comision2.pdf)** | Texto explicativo del proceso, con Modelado de negocio, arquitectura y programación, documentación y calidad. |
| **[Graficos BPMN 2.0](./BPMN2.0)** | Diagramas:  BPMN 2.0 (AS-IS) del proceso de recepción (manual) y BPMN 2.0 (TO-BE) del proceso de recepción con ChatBot. |
| **[Diagrama  BPMN 2.0 (AS-IS)](.BPMN2.0/TurneroAtencion-BPMN(AS-IS).png)** | Describe el proceso de recepción (manual). |
| **[Diagrama  BPMN 2.0 (TO-BE)](.BPMN2.0/TurneroAtencion-BPMN(TO-BE)(2.0).png)** | Describe el proceso de recepción con el ChatBot de turnos. |
| **[Máquina de Estado Finito (FSM)(./BPMN2.0/TurneroAtencion-FSM.png)** | Describe la Máquina de Estado Finito (FSM) desarrollada para este chatbot. |


---

## 📦 Archivos del Proyecto

| Archivo | Descripción |
|---------|-------------|
| **[main_chatbot_turnos.py](./main_chatbot_turnos.py)** | Programa principal del chatbot. Máquina de estados FSM que gestiona el flujo de atención al paciente. |
| **[generar_turnos_tickets_aleatorios.py](./generar_turnos_tickets_aleatorios.py)** | Script para generar datos de prueba. Crea turnos y tickets aleatorios en archivos CSV. |
| **[MANUAL_DE_USUARIO.md](./MANUAL_DE_USUARIO.md)** | Guía completa para usar el chatbot. Incluye instrucciones paso a paso y ejemplos. |
| **[DICCIONARIO_DE_DATOS.md](./DICCIONARIO_DE_DATOS.md)** | Documentación técnica de estructuras de datos, variables y archivos CSV utilizados. |
| **[turnos.csv](./turnos.csv)** | Base de datos de turnos pre-asignados a pacientes (entrada del sistema). |
| **[tickets.csv](./tickets.csv)** | Registro de todos los tickets generados (salida del sistema). |

---

## ⚙️ Requisitos Previos

- **Python:** 3.8 o superior
- **Librerías:**
  - `rich` (para interfaz visual mejorada)
  - `pathlib` (incluida en Python)
  - `csv` (incluida en Python)
  - `datetime` (incluida en Python)

### Instalación de dependencias:

```bash
pip install rich
```

---

## 🚀 Uso Rápido

1. **Ejecutar el chatbot:**
   ```bash
   python main_chatbot_turnos.py
   ```

2. **Generar datos de prueba:**
   ```bash
   python generar_turnos_tickets_aleatorios.py
   ```

3. **Consultar documentación:**
   - Para instrucciones de usuario: Ver [MANUAL_DE_USUARIO.md](./MANUAL_DE_USUARIO.md)
   - Para detalles técnicos: Ver [DICCIONARIO_DE_DATOS.md](./DICCIONARIO_DE_DATOS.md)

---

## 💻 Compatibilidad

- ✅ Linux / macOS
- ✅ Windows (con Windows Terminal o PowerShell moderno para ver colores)

---

## 📋 Especialidades Disponibles

Clínica General · Pediatría · Traumatología · Cardiología · Neurología · Dermatología · Psicología · ORL · Otras consultas

---

**Generado con asistencia de GitHub Copilot**
