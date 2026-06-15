# 📖 Manual de Usuario - Sistema de Atención con Turnos

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

## 📌 Índice
1. [Inicio rápido](#inicio-rápido)
2. [Pantallas principales](#pantallas-principales)
3. [Flujos de uso](#flujos-de-uso)
4. [Comandos y teclas](#comandos-y-teclas)
5. [Preguntas frecuentes](#preguntas-frecuentes)
6. [Solución de problemas](#solución-de-problemas)

---

## 🚀 Inicio Rápido

### Ejecutar el programa
```bash
cd /ruta/del/proyecto/Codigo_ChatBot
python3 main_chatbot_turnos.py
```

### Pantalla de bienvenida
```
╭──────────────────────────────────────────────────────╮
│  🏥 CENTRO MÉDICO INTEGRAL 🏥                        │
│  Sistema de Atención con Turnos                      │
╰──────────────────────────────────────────────────────╯

Presione Enter para continuar o ESC para salir.
```

**Acciones disponibles:**
- **Enter (↵):** Comenzar nuevo turno
- **ESC:** Salir del programa

---

## 📺 Pantallas Principales

### 1️⃣ Validación de DNI

```
╭──────────────────────────╮
│  🆔 Validación de DNI    │
╰──────────────────────────╯

Para ser atendido debe ingresar su DNI.

────────────────────────────────────────────────────
    Ingrese (8 dígitos sin puntos ni espacios): _
```

**Qué ingresar:**
- 8 dígitos de su Documento Nacional de Identidad
- Sin puntos, sin espacios, sin caracteres especiales
- Ejemplo: `30236685`

**Validaciones:**
- ✓ Válido: números entre 1,000,000 y 99,999,999
- ✗ Inválido: menos de 7 dígitos
- ✗ Inválido: más de 8 dígitos
- ✗ Inválido: contiene letras o caracteres especiales

**Mensaje de confirmación:**
```
    ✓ DNI válido: 30236685
```

---

### 2️⃣ Pregunta de Turno Previo

```
❓ ¿Tiene un turno previamente asignado?
  1 - SÍ
  2 - NO
  0 - CANCELAR Y VOLVER AL INICIO

→ Seleccione opción (0-2):
```

**Opciones:**
| Opción | Acción |
|--------|--------|
| `1` | Tengo un turno registrado en el sistema |
| `2` | No tengo turno previo |
| `0` | Cancelar y volver al inicio |

**Resultado según selección:**

- **Si elige 1 (SÍ):**
  ```
  El sistema busca su DNI en los turnos registrados.
  ├─ Turno encontrado → Muestra datos del turno
  └─ Turno NO encontrado → Se asigna sin turno
  ```

- **Si elige 2 (NO):**
  ```
  Se le presenta directamente el menú de especialidades
  ```

- **Si elige 0:**
  ```
  ╭─────────────────────────────────────────╮
  │ Proceso cancelado. Volviendo al inicio... │
  ╰─────────────────────────────────────────╯
  ```

---

### 3️⃣ Turno Encontrado (si aplica)

```
┌──────────────────────────────────────────────────────┐
│                   📄 Turno Encontrado                │
├──────────────────────────────────────────────────────┤
│ Campo         │ Valor                               │
├───────────────┼─────────────────────────────────────┤
│ DNI           │ 30236685                            │
│ Nombre        │ Juan García                         │
│ Especialidad  │ Clínica General                     │
│ Fecha         │ 2026-06-20                          │
│ Hora          │ 14:30                               │
└──────────────────────────────────────────────────────┘
```

**Información mostrada:**
- ✓ DNI confirmado
- ✓ Nombre y apellido del paciente
- ✓ Especialidad asignada
- ✓ Fecha del turno
- ✓ Hora del turno

**Siguiente paso:** Se pregunta sobre cobertura de obra social

---

### 4️⃣ Menú de Especialidades

```
┏━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Opción ┃ Especialidad           ┃ Código ┃
┡━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1      │ Clínica General        │ CG     │
│ 2      │ Pediatría              │ PD     │
│ 3      │ Traumatología          │ TR     │
│ 4      │ Cardiología            │ CA     │
│ 5      │ Neurología             │ NE     │
│ 6      │ Dermatología           │ DE     │
│ 7      │ Psicología             │ PS     │
│ 8      │ ORL                    │ OR     │
│ 9      │ Otras consultas        │ OC     │
│ 0      │ Salir de la aplicación │ ─      │
└────────┴────────────────────────┴────────┘

Elija una especialidad médica para ser atendido:
→ Seleccione opción (0-9): _
```

**Cómo usar:**
1. Busque la especialidad que desea
2. Ingrese el número de opción correspondiente
3. Presione Enter

**Ejemplo:**
```
→ Seleccione opción (0-9): 1

✓ Usted eligió: Clínica General
```

**Especialidades disponibles:**
- `1` - Clínica General
- `2` - Pediatría
- `3` - Traumatología
- `4` - Cardiología
- `5` - Neurología
- `6` - Dermatología
- `7` - Psicología
- `8` - ORL (Otorrinolaringología)
- `9` - Otras consultas
- `0` - Salir del programa

---

### 5️⃣ Pregunta de Obra Social

```
❓ ¿Posee obra social?
  1 - SÍ
  2 - NO
  0 - CANCELAR Y VOLVER AL INICIO

→ Seleccione opción (0-2):
```

**Opciones:**
| Opción | Significado |
|--------|-------------|
| `1` | Sí, tengo cobertura médica |
| `2` | No, no tengo cobertura |
| `0` | Cancelar la solicitud |

**En el ticket mostrará:**
- Si elige 1 (SÍ): `Obra Social: Con cobertura`
- Si elige 2 (NO): `Obra Social: Sin cobertura`

---

### 6️⃣ Ticket de Atención

```
════════════════════════════════════════════════════════
      Generando su número de atención
════════════════════════════════════════════════════════

┌──────────────────────────────────────────────────────┐
│                                                       │
│              CENTRO MÉDICO INTEGRAL                  │
│               Número de Atención                     │
│                                                       │
│                      CG002                           │
│                                                       │
├──────────────────────────────────────────────────────┤
│ Especialidad: Clínica General                         │
│ DNI del paciente: 30236685                            │
│ Con turno: Sí                                         │
│ Obra Social: Con cobertura                            │
│ Fecha: 14/06/2026                                     │
│ Hora: 16:58                                           │
│                                                       │
└──────────────────────────────────────────────────────┘

╭──────────────────────────────────────────────────────╮
│ ✓ Será llamado por la pantalla en la sala de espera  │
╰──────────────────────────────────────────────────────╯

⚠ Guarde este número para referencia
```

**Información del ticket:**
- **Número de atención:** Código única de 4-5 caracteres (ej: `CG002`)
- **Especialidad:** La seleccionada por el usuario
- **DNI:** Confirmado al inicio
- **Con turno:** Sí/No según origen de la solicitud
- **Obra Social:** Tipo de cobertura
- **Fecha:** Día actual en formato DD/MM/YYYY
- **Hora:** Hora actual en formato HH:MM

**Instrucciones:**
- ✓ Guarde o anote el número de atención
- ✓ Espere a que lo llamen en la sala de espera
- ✓ Atienda cuando escuche su número en la pantalla

---

## 🔄 Flujos de Uso

### Flujo 1: Usuario CON Turno Registrado

```
1. Ejecutar programa
           ↓
2. Presionar Enter
           ↓
3. Ingresar DNI (ej: 30236685)
           ↓
4. Seleccionar opción 1 (¿Tiene turno?)
           ↓
5. Sistema busca DNI en turnos.csv
           ↓
   ┌─────────────────────────┬──────────────────┐
   │ Turno encontrado        │ Turno NO encontrado
   ├─────────────────────────┼──────────────────┤
   │ Se muestra turno        │ Se indica que no existe
   │ Especialidad automática │ Se pide seleccionar
   │                         │ especialidad
   └─────────────────────────┴──────────────────┘
           ↓
6. Seleccionar opción sobre obra social (1-2)
           ↓
7. Sistema genera ticket (ej: CG002)
           ↓
8. Mostrar ticket en pantalla
           ↓
9. Volver a pantalla de inicio (siguiente usuario)
```

### Flujo 2: Usuario SIN Turno Registrado

```
1. Ejecutar programa
           ↓
2. Presionar Enter
           ↓
3. Ingresar DNI (ej: 23456789)
           ↓
4. Seleccionar opción 2 (¿Tiene turno?)
           ↓
5. Seleccionar especialidad del menú (1-9)
   ├─ 1: Clínica General
   ├─ 2: Pediatría
   ├─ 3: Traumatología
   └─ ... etc
           ↓
6. Seleccionar opción sobre obra social (1-2)
           ↓
7. Sistema genera ticket (ej: PD001)
           ↓
8. Mostrar ticket en pantalla
           ↓
9. Volver a pantalla de inicio (siguiente usuario)
```

### Flujo 3: Cancelar una Solicitud

```
En cualquier momento del proceso:
Seleccionar opción 0 (CANCELAR)
           ↓
╭──────────────────────────────────────────╮
│ Proceso cancelado. Volviendo al inicio... │
╰──────────────────────────────────────────╯
           ↓
Pantalla de bienvenida (siguiente usuario)
```

---

## ⌨️ Comandos y Teclas

### Navegación General

| Tecla | Acción |
|-------|--------|
| **Enter (↵)** | Confirmar, aceptar, continuar |
| **0-9** | Seleccionar opción en menúes |
| **ESC** | Salir del programa (solo en pantalla de inicio) |
| **Backspace** | Borrar último carácter (en entrada de texto) |

### Opciones Numéricas

**En preguntas Sí/No:**
- `1` → SÍ (color verde)
- `2` → NO (color rojo)
- `0` → CANCELAR (volver al inicio)

**En menú de especialidades:**
- `1` → Clínica General
- `2` → Pediatría
- ... (ver tabla anterior)
- `0` → Salir de la aplicación

**En validaciones:**
- Solo se aceptan números válidos
- Si ingresa número fuera de rango, se vuelve a solicitar
- Si ingresa letra, se muestra error

---

## ❓ Preguntas Frecuentes

### ¿Qué debo hacer si olvido mi número de atención?

**R:** El número aparece en la pantalla solo una vez. Se recomienda:
- ✓ Escribir o fotografiar el número inmediatamente
- ✓ No abandonar la pantalla hasta anotarlo
- Si olvidó el número, deberá solicitar un nuevo ticket comenzando de nuevo

---

### ¿Puedo cambiar mi especialidad después de seleccionarla?

**R:** No directamente. Si desea cambiar:
1. Cancelar la solicitud actual (opción 0)
2. Comenzar un nuevo trámite
3. Seleccionar la especialidad correcta

---

### ¿Qué pasa si ingreso un DNI inválido?

**R:** El sistema rechazará el DNI si:
- Tiene menos de 7 dígitos → "El número del DNI ingresado es muy chico"
- Tiene más de 8 dígitos → "El número del DNI ingresado es muy grande"
- Contiene letras → "Eso no parece un número"

Intente ingresando nuevamente con 8 dígitos válidos.

---

### ¿Tengo que ir sí o sí a la hora que figura en el ticket?

**R:** Depende:
- **Si tiene turno previo:** Sí, debe respetar la hora del turno
- **Si no tiene turno previo:** Se le asignará un número de espera. Aguarde a ser llamado en la sala de espera

---

### ¿Cómo se diferencia entre tener turno o no en el sistema?

**R:** En el ticket verá:
- `Con turno: Sí` → Tenía un turno previamente asignado
- `Con turno: No` → Fue atendido sin turno previo (número de espera)

---

### ¿Puedo volver a usar el mismo DNI para otro turno?

**R:** Sí. Cada vez que ejecute el programa:
- Es una nueva sesión
- Puede ingresar un DNI diferente
- O el mismo DNI para un trámite diferente

---

## 🔧 Solución de Problemas

### El programa no inicia

**Problema:** Error `ModuleNotFoundError: No module named 'rich'`

**Solución:**
```bash
pip install rich
```
O si usa Python 3:
```bash
pip3 install rich
```

---

### Los caracteres especiales se ven extraños

**Problema:** Algunos bordes o emojis se muestran incorrectamente

**Posible causa:** Terminal no soporta UTF-8

**Soluciones:**
1. Usar terminal con soporte UTF-8 (recomendado en Linux/Mac)
2. En Windows, usar Windows Terminal en lugar de CMD

---

### Los colores no se ven

**Problema:** El texto no aparece coloreado

**Posible causa:** Terminal no soporta colores ANSI

**Solución:**
- Actualizar terminal
- En Linux: usar `gnome-terminal`, `konsole`, o `xterm`
- En Windows: usar Windows Terminal

---

### El programa se cierra inesperadamente

**Problema:** El programa termina sin razón aparente

**Posibles causas:**
- Presionó ESC en la pantalla de inicio
- Presionó Ctrl+C en la terminal
- Error interno (contactar al desarrollador)

---

### El archivo turnos.csv no se crea

**Problema:** Error al buscar turnos

**Solución:**
- Verificar permisos de escritura en la carpeta
- Asegurarse de ejecutar el programa desde el directorio correcto:
  ```bash
  cd /ruta/del/proyecto/Codigo_ChatBot
  python3 main_chatbot_turnos.py
  ```

---

### Números de atención duplicados o incorrectos

**Problema:** Aparecen números repetidos en los tickets

**Solución:**
- Eliminar o respaldar el archivo `tickets.csv`
- Ejecutar nuevamente el programa
- Los números se regenerarán correctamente

---

## 📊 Estadísticas Útiles

### Número de Atención - Formato

**Estructura:** `[CÓDIGO_ESPECIALIDAD][NÚMERO_CORRELATIVO]`

**Ejemplos:**
- `CG001` - Primer ticket de Clínica General
- `CG002` - Segundo ticket de Clínica General
- `PD001` - Primer ticket de Pediatría
- `TR005` - Quinto ticket de Traumatología

**Cada especialidad tiene su propia numeración correlativa.**

---

## 📞 Contacto y Soporte

Para reportar problemas o sugerencias:
- Verificar documentación en `DICCIONARIO_DE_DATOS.md`
- Revisar archivo de código `main_chatbot_turnos.py`
- Contactar al administrador del sistema

---

**Documento generado con asistencia de GitHub Copilot**

---

Este manual se escribió considerando:
- Usuarios sin experiencia técnica
- Instrucciones claras y paso a paso
- Ejemplos reales de uso
- Solución de problemas comunes
```