# 🏢 Sistema de Gestión de Permisos RRHH — UNEMI

Sistema de gestión de permisos laborales desarrollado en **Python puro**, aplicando los principios de la **Programación Orientada a Objetos (POO)**: herencia, encapsulamiento, abstracción, polimorfismo, mixins y decoradores. La interfaz es completamente por consola con colores ANSI y la persistencia de datos se realiza en archivos **JSON**.

---

## 📋 Tabla de contenidos

- [Características](#-características)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Arquitectura y diseño](#-arquitectura-y-diseño)
- [Modelos de datos](#-modelos-de-datos)
- [Módulo Core](#-módulo-core)
- [Controladores](#-controladores)
- [Vista](#-vista)
- [Persistencia](#-persistencia-json)
- [Cómo ejecutar](#-cómo-ejecutar)
- [Uso del sistema](#-uso-del-sistema)
- [Validaciones implementadas](#-validaciones-implementadas)
- [Ejemplos de datos](#-ejemplos-de-datos)

---

## ✨ Características

- CRUD completo para **Empleados**, **Tipos de Permiso** y **Solicitudes de Permiso**
- Cálculo automático de **descuentos** en permisos no remunerados (basado en valor/hora)
- **Validaciones robustas** con decoradores: nombre, cédula ecuatoriana (módulo 10), número, fecha, S/N, D/H
- Interfaz de consola **colorida** con ANSI codes
- Persistencia automática en **archivos JSON**
- Estadísticas y reportes: total empleados, tiempo acumulado, permisos remunerados/no remunerados, monto a descontar
- Protección de integridad: no se puede eliminar un empleado con permisos activos
- Arquitectura en capas clara: **Vista → Controlador → Modelo → Persistencia**

---

## 📁 Estructura del proyecto

```
S_Tarea_POO_main/
│
├── main.py                          # Punto de entrada del programa
│
├── models/                          # Capa de dominio (modelos)
│   ├── __init__.py
│   ├── employee.py                  # Clase Empleado
│   ├── permission_type.py           # Clase TipoPermiso
│   └── permission.py                # Clase Permiso
│
├── controllers/                     # Capa de lógica de negocio
│   ├── __init__.py
│   ├── system_controller.py         # Controlador central (facade)
│   ├── employee_controller.py       # CRUD de empleados
│   ├── permission_type_controller.py# CRUD de tipos de permiso
│   ├── permission_controller.py     # CRUD de solicitudes de permiso
│   └── menu_controller.py           # Controlador del menú principal
│
├── views/                           # Capa de presentación
│   ├── __init__.py
│   └── console_view.py              # Interfaz de usuario por consola
│
├── core/                            # Núcleo: interfaces, mixins, decoradores
│   ├── __init__.py
│   ├── interfaces.py                # Interfaz abstracta ICrud
│   ├── mixins.py                    # EstadisticasMixin, ValidationMixin, LogMixin
│   ├── decoradores.py               # Decoradores de validación de entrada
│   └── json_manager.py              # Gestor de persistencia JSON
│
└── data/                            # Archivos de datos (generados automáticamente)
    ├── employees.json
    ├── permission_types.json
    └── permissions.json
```

---

## 🏗️ Arquitectura y diseño

El sistema implementa una arquitectura **MVC (Modelo-Vista-Controlador)** con separación clara de responsabilidades:

```
main.py
  └── MenuController          ← orquesta el flujo del menú
        ├── ConsoleView        ← toda la entrada/salida de usuario
        └── SystemController   ← facade central que delega a sub-controladores
              ├── EmployeeController
              ├── PermissionTypeController
              └── PermissionController
                    └── JsonManager   ← persistencia en .json
```

### Principios POO aplicados

| Principio           | Dónde se aplica                                                                                             |
| ------------------- | ----------------------------------------------------------------------------------------------------------- |
| **Abstracción**     | `ICrud` (ABC) define el contrato CRUD que todos los controladores deben cumplir                             |
| **Herencia**        | `SystemController(ICrud, EstadisticasMixin)`, `EmployeeController(ICrud, ValidationMixin, LogMixin)`        |
| **Encapsulamiento** | `sueldo` en `Empleado` usa `@property` y `@sueldo.setter` con validación; atributo privado `__sueldo`       |
| **Polimorfismo**    | `sistema.crear(dato)` acepta `Empleado`, `TipoPermiso` o `Permiso` y delega según tipo                      |
| **Mixins**          | `EstadisticasMixin` aporta estadísticas, `ValidationMixin` aporta validaciones, `LogMixin` aporta logging   |
| **Decoradores**     | `@validar_nombre`, `@validar_cedula`, `@validar_numero`, etc. envuelven métodos de entrada en `ConsoleView` |

---

## 📦 Modelos de datos

### `Empleado` — `models/employee.py`

```python
Empleado(id, nombre, sueldo, cedula)
```

| Atributo     | Tipo             | Descripción                                       |
| ------------ | ---------------- | ------------------------------------------------- |
| `id`         | int              | Identificador único autoincremental               |
| `nombre`     | str              | Nombre completo (mínimo nombre + apellido)        |
| `sueldo`     | float (property) | Sueldo mensual. Setter valida que no sea negativo |
| `cedula`     | str              | Cédula ecuatoriana de 10 dígitos                  |
| `valor_hora` | float            | Calculado automáticamente: `sueldo / 240`         |

**Métodos:** `a_dic()` → serializa a dict · `from_dict(datos)` → deserializa desde JSON

---

### `TipoPermiso` — `models/permission_type.py`

```python
TipoPermiso(id, descripcion, remunerado)
```

| Atributo      | Tipo | Descripción                                  |
| ------------- | ---- | -------------------------------------------- |
| `id`          | int  | Identificador único                          |
| `descripcion` | str  | Ej: "Vacaciones", "Matrimonio", "Enfermedad" |
| `remunerado`  | str  | `"S"` (sí) o `"N"` (no)                      |

**Métodos:** `a_dic()` · `from_dict(datos)`

---

### `Permiso` — `models/permission.py`

```python
Permiso(id, id_empleado, id_tipo_permiso, fecha_desde, fecha_hasta, tipo, tiempo, descuento=0.0)
```

| Atributo          | Tipo  | Descripción                                   |
| ----------------- | ----- | --------------------------------------------- |
| `id`              | int   | Identificador único                           |
| `id_empleado`     | int   | FK → Empleado                                 |
| `id_tipo_permiso` | int   | FK → TipoPermiso                              |
| `fecha_desde`     | str   | Formato `DD/MM/YYYY`                          |
| `fecha_hasta`     | str   | Formato `DD/MM/YYYY` (debe ser ≥ fecha_desde) |
| `tipo`            | str   | `"D"` (días) o `"H"` (horas)                  |
| `tiempo`          | int   | Cantidad de días u horas                      |
| `descuento`       | float | Monto descontado (0.0 si es remunerado)       |

**Método clave:**

```python
def calcular_descuento(self, valor_hora):
    # tipo "H": tiempo * valor_hora
    # tipo "D": tiempo * 8 * valor_hora
    self.descuento = round(monto, 2)
    return self.descuento
```

---

## ⚙️ Módulo Core

### `ICrud` — `core/interfaces.py`

Interfaz abstracta (ABC) que obliga a implementar las 4 operaciones CRUD:

```python
class ICrud(ABC):
    @abstractmethod def crear(self, dato): ...
    @abstractmethod def consultar(self): ...
    @abstractmethod def actualizar(self, categoria, id_buscar, nuevos_datos): ...
    @abstractmethod def eliminar(self, categoria, id): ...
```

---

### `Mixins` — `core/mixins.py`

| Mixin               | Métodos                                                                                                 | Uso                              |
| ------------------- | ------------------------------------------------------------------------------------------------------- | -------------------------------- |
| `EstadisticasMixin` | `calcular_total_empleados()`, `calcular_total_permisos()`, `calcular_tiempo()`, `calcular_descuentos()` | Heredado por `SystemController`  |
| `ValidationMixin`   | `validate_not_empty()`, `validate_positive_number()`                                                    | Heredado por sub-controladores   |
| `LogMixin`          | `log(message)`                                                                                          | Mensajes de auditoría en consola |

---

### `Decoradores` — `core/decoradores.py`

Cada decorador envuelve un método de `ConsoleView` en un **loop** que repite la solicitud hasta recibir una entrada válida, mostrando el error con `error_y_pausa()`.

| Decorador         | Valida                                                        |
| ----------------- | ------------------------------------------------------------- |
| `@validar_nombre` | Mínimo nombre + apellido, solo letras y tildes                |
| `@validar_cedula` | 10 dígitos, provincia válida (01-24), algoritmo **módulo 10** |
| `@validar_numero` | Número flotante positivo                                      |
| `@validar_fecha`  | Formato `DD/MM/YYYY` con fecha lógica                         |
| `@validar_texto`  | No vacío, debe contener al menos una letra                    |
| `@validar_d_h`    | Solo acepta `D` o `H`                                         |
| `@validar_s_n`    | Solo acepta `S` o `N`                                         |

---

### `JsonManager` — `core/json_manager.py`

Gestiona la lectura y escritura de los archivos JSON:

```python
class JsonManager:
    def load(self) -> list   # Carga la lista desde el archivo (retorna [] si no existe)
    def save(self, data)     # Serializa y guarda con indent=4 y ensure_ascii=False
```

Crea automáticamente el directorio `data/` si no existe.

---

## 🎛️ Controladores

### `SystemController` — Fachada central

Hereda de `ICrud` y `EstadisticasMixin`. Es el único punto de contacto entre el menú y la lógica de negocio. Delega cada operación al sub-controlador correspondiente según el tipo del objeto recibido.

```python
sistema.crear(Empleado(...))      # → EmployeeController.crear()
sistema.crear(TipoPermiso(...))   # → PermissionTypeController.crear()
sistema.crear(Permiso(...))       # → PermissionController.crear()

sistema.actualizar('A', id, datos)  # A=Empleado, B=TipoPermiso, C=Permiso
sistema.eliminar('B', id)
```

Expone propiedades `empleados`, `tipos_permiso` y `permisos` que delegan a sus sub-controladores.

---

### `MenuController` — Flujo del menú

Mantiene el loop principal del sistema y mapea cada opción del menú (1–6) a un método privado:

| Opción | Método            | Descripción                                                     |
| ------ | ----------------- | --------------------------------------------------------------- |
| 1      | `_registrar()`    | Sub-menú A/B/C para registrar Empleado, TipoPermiso o Solicitud |
| 2      | `_consultar()`    | Muestra todos los registros                                     |
| 3      | `_eliminar()`     | Elimina por ID con validación de integridad                     |
| 4      | `_modificar()`    | Actualiza campos de un registro existente                       |
| 5      | `_estadisticas()` | Genera reportes con `EstadisticasMixin`                         |
| 6      | `_salir()`        | Termina el loop y cierra el sistema                             |

> **Integridad referencial:** antes de eliminar un empleado, verifica que no tenga solicitudes de permiso activas. Si las tiene, bloquea la eliminación e informa al usuario.

---

## 🖥️ Vista

### `ConsoleView` — `views/console_view.py`

Maneja toda la entrada/salida de usuario. Usa **códigos ANSI** para colores y la clase auxiliar `Color` para centralizar los estilos.

Los métodos de entrada están decorados para validación automática:

```python
@validar_nombre  def obtener_nombre(self)      → str
@validar_cedula  def obtener_cedula(self)       → str
@validar_numero  def obtener_sueldo(self)       → float
@validar_fecha   def obtener_fecha_inicio(self) → str
@validar_d_h     def obtener_d_h(self)          → str  ("D" o "H")
@validar_s_n     def obtener_s_n(self)          → str  ("S" o "N")
```

Al registrar una solicitud de permiso, muestra un **resumen previo** con el descuento calculado antes de confirmar el guardado.

---

## 💾 Persistencia JSON

Los datos se guardan automáticamente en la carpeta `data/` cada vez que se realiza una operación de escritura.

### `data/employees.json`

```json
[
  {
    "id": 1,
    "nombre": "Isaac Silva",
    "sueldo": 2000.0,
    "cedula": "1250145701"
  }
]
```

### `data/permission_types.json`

```json
[
  {
    "id": 1,
    "descripcion": "Matrimonio",
    "remunerado": "S"
  }
]
```

### `data/permissions.json`

```json
[
  {
    "id": 1,
    "id_empleado": 1,
    "id_tipo_permiso": 1,
    "fecha_desde": "20/04/2025",
    "fecha_hasta": "25/04/2025",
    "tipo": "D",
    "tiempo": 5,
    "descuento": 0.0
  }
]
```

---

## 🚀 Cómo ejecutar

### Requisitos

- **Python 3.10+** (no requiere librerías externas)
- Terminal con soporte de colores ANSI (cualquier terminal en Linux/Mac; en Windows usar Windows Terminal o VS Code)

### Pasos

```bash
# 1. Clonar o descomprimir el proyecto
cd S_Tarea_POO_main

# 2. Ejecutar directamente
python main.py
```

> La carpeta `data/` y los archivos `.json` se crean automáticamente al registrar el primer elemento.

---

## 📖 Uso del sistema

Al iniciar, se muestra el menú principal:

```
══════════════════════════════════════════════════
          SISTEMA DE GESTIÓN RRHH - UNEMI
══════════════════════════════════════════════════
  [1]  Registrar Nuevo Empleado
  [2]  Consultar Registros
  [3]  Eliminar Registro por ID
  [4]  Modificar Registro
  [5]  Ver Estadísticas y Reportes
  [6]  Salir
══════════════════════════════════════════════════
  Elija una opción (1-6):
```

### Flujo de registro (opción 1)

```
¿Qué desea registrar? [A] Empleado | [B] Tipo Permiso | [C] Solicitud | [R] Regresar
```

- **A – Empleado:** pide nombre, cédula y sueldo. Valida cédula con módulo 10 y unicidad.
- **B – Tipo Permiso:** pide descripción y si es remunerado (S/N).
- **C – Solicitud:** muestra la lista de empleados y tipos disponibles, pide fechas, tipo (D/H) y tiempo. Calcula y muestra el descuento antes de confirmar.

### Estadísticas (opción 5)

Genera un reporte con:

- Total de empleados en nómina
- Total de días y horas acumulados en permisos
- Permisos remunerados vs. no remunerados
- **Monto total a descontar** de los permisos no remunerados

---

## ✅ Validaciones implementadas

| Campo                | Regla                                                        |
| -------------------- | ------------------------------------------------------------ |
| Nombre               | Mínimo 2 palabras, solo letras y tildes                      |
| Cédula               | 10 dígitos, provincia 01–24, algoritmo módulo 10 ecuatoriano |
| Sueldo / Tiempo      | Número positivo mayor a 0                                    |
| Fecha                | Formato `DD/MM/YYYY`, fecha lógica válida                    |
| Fecha fin            | Debe ser mayor o igual a la fecha de inicio                  |
| Tipo tiempo          | Solo `D` (días) o `H` (horas)                                |
| Remunerado           | Solo `S` o `N`                                               |
| Cédula duplicada     | No se permite registrar dos empleados con la misma cédula    |
| Eliminación empleado | Bloqueada si el empleado tiene solicitudes activas           |

---

## 👨‍💻 Autor

Proyecto académico desarrollado para la materia de **Programación Orientada a Objetos** — Universidad Estatal de Milagro (UNEMI).
