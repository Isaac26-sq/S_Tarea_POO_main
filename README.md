#  Sistema de Gestión de RRHH — UNEMI

Sistema de consola desarrollado en **Python** para la gestión de permisos laborales del personal. Permite registrar empleados, tipos de permiso y solicitudes de permiso, con cálculo automático de descuentos por permisos no remunerados. Aplicado bajo el paradigma de **Programación Orientada a Objetos (POO)**.

---
##  Chat de ia usada para la tarea

https://gemini.google.com/share/119131a81361



##  Estructura del Proyecto

```
S_Tarea_POO_main/
│
├── main.py                        # Punto de entrada del sistema
│
├── models/                        # Clases de dominio (entidades)
│   ├── employee.py                # Clase Empleado
│   ├── permission.py              # Clase Permiso (solicitud)
│   └── permission_type.py        # Clase TipoPermiso
│
├── core/                          # Lógica base y utilidades
│   ├── interfaces.py              # Interfaz abstracta ICrud
│   ├── mixins.py                  # EstadisticasMixin (reportes)
│   ├── decoradores.py             # Decoradores de validación
│   └── json_manager.py           # Gestión de persistencia JSON
│
├── controllers/
│   └── system_controller.py      # Controlador principal del sistema
│
├── views/
│   └── console_view.py           # Vista de consola (UI)
│
├── data/                          # Archivos de datos (persistencia)
│   ├── employees.json
│   ├── permissions.json
│   └── permission_types.json
│
└── docs/                          # Diagramas del sistema
    ├── Diagrama de clases.excalidraw
    └── Diagrama de procesos.excalidraw
```

---

## 🚀 Cómo Ejecutar

**Requisitos:** Python 3.10 o superior.

```bash

cd S_Tarea_POO_main


python main.py
```

> El sistema carga automáticamente los datos desde los archivos JSON en la carpeta `data/` al iniciar.

---

## Funcionalidades del Menú
 
| Opción | Descripción |
|--------|-------------|
| **1** | Registrar nuevo Empleado, Tipo de Permiso o Solicitud |
| **2** | Consultar todos los registros del sistema |
| **3** | Eliminar un registro por ID |
| **4** | Modificar un registro existente |
| **5** | Ver estadísticas y reportes financieros |
| **6** | Salir del sistema |

---

##  Arquitectura — Patrón MVC

El proyecto sigue el patrón **Modelo - Vista - Controlador**:

- **Modelo** (`models/`): Las clases de datos del negocio.
- **Vista** (`views/`): La interfaz de consola que interactúa con el usuario.
- **Controlador** (`controllers/`): Orquesta la lógica entre vista y modelos.

---

##  Módulos y Clases

---

### `models/employee.py` — Clase `Empleado`

Representa a un trabajador del sistema.

**Atributos:**

| Atributo | Tipo | Descripción |
|----------|------|-------------|
| `id` | `int` | Identificador único |
| `nombre` | `str` | Nombre completo |
| `sueldo` | `float` | Sueldo mensual (validado, no puede ser negativo) |
| `cedula` | `str` | Cédula ecuatoriana |
| `valor_hora` | `float` | Calculado automáticamente: `sueldo / 240` |

**Métodos:**

- `sueldo` *(property/setter)*: Valida que el sueldo no sea negativo y recalcula `valor_hora`.
- `a_dic()`: Convierte el objeto a diccionario para serialización JSON.
- `from_dict(datos)` — reconstruye el objeto desde un diccionario JSON

---

### `models/permission_type.py` — Clase `TipoPermiso`

Define las categorías de permisos disponibles en el sistema.

**Atributos:**

| Atributo | Tipo | Descripción |
|----------|------|-------------|
| `id` | `int` | Identificador único |
| `descripcion` | `str` | Nombre o descripción del tipo |
| `remunerado` | `str` | `'S'` si es remunerado, `'N'` si no lo es |

**Métodos:**

- `a_dic()`: Convierte el objeto a diccionario para serialización JSON.
- `from_dict(datos)` — reconstruye el objeto desde un diccionario JSON
---

### `models/permission.py` — Clase `Permiso`

Representa una solicitud de permiso realizada por un empleado.

**Atributos:**

| Atributo | Tipo | Descripción |
|----------|------|-------------|
| `id` | `int` | Identificador único |
| `id_empleado` | `int` | ID del empleado que solicita |
| `id_tipo_permiso` | `int` | ID del tipo de permiso |
| `fecha_desde` | `str` | Fecha de inicio (`DD/MM/YYYY`) |
| `fecha_hasta` | `str` | Fecha de fin (`DD/MM/YYYY`) |
| `tipo` | `str` | `'D'` para días, `'H'` para horas |
| `tiempo` | `int` | Cantidad de días u horas solicitadas |

**Métodos:**

- `a_dic()`: Convierte el objeto a diccionario para serialización JSON.
- `from_dict(datos)` — reconstruye el objeto desde un diccionario JSON
---

### `core/interfaces.py` — Interfaz `ICrud`

Clase abstracta que define el contrato CRUD que debe implementar el controlador.

```python
from abc import ABC, abstractmethod

class ICrud(ABC):
    @abstractmethod
    def crear(self, dato): ...

    @abstractmethod
    def actualizar(self, categoria, id_buscar, nuevos_datos): ...

    @abstractmethod
    def consultar(self): ...

    @abstractmethod
    def eliminar(self, categoria, id): ...
```

---

### `core/mixins.py` — Clase `EstadisticasMixin`

Mixin que agrega funcionalidades de reportes y estadísticas al controlador.

**Métodos:**

| Método | Descripción |
|--------|-------------|
| `calcular_total_empleados(lista)` | Imprime el total de empleados en nómina |
| `calcular_total_permisos(permisos, tipos)` | Total de permisos, separados en remunerados y no remunerados |
| `calcular_tiempo(permisos)` | Suma total de días y horas de permisos |
| `calcular_descuentos(permisos, tipos, empleados)` | Calcula el monto total a descontar por permisos no remunerados, usando `valor_hora` del empleado |

**Lógica de descuento:**
- Permiso en **horas**: `descuento = tiempo × valor_hora`
- Permiso en **días**: `descuento = tiempo × 8 × valor_hora`

---

### `core/decoradores.py` — Decoradores de Validación

Decoradores que envuelven métodos de entrada para garantizar datos correctos. Si el dato es inválido, repiten el pedido automáticamente.

| Decorador | Valida |
|-----------|--------|
| `@validar_nombre` | Solo letras y espacios, no vacío |
| `@validar_texto` | Texto no vacío con al menos una letra |
| `@validar_numero` | Número flotante mayor a 0 |
| `@validar_fecha` | Formato `DD/MM/YYYY` válido |
| `@validar_D_H` | Solo acepta `'D'` o `'H'` |
| `@validar_S_N` | Solo acepta `'S'` o `'N'` |
| `@validar_cedula` | Cédula ecuatoriana válida (10 dígitos, provincia 01–24, Módulo 10) |

**Ejemplo de uso:**
```python
@validar_numero
def obtener_sueldo(self):
    return input("Sueldo mensual ($): ")
```

---

### `core/json_manager.py` — Clase `JsonManager`

Maneja la persistencia de datos en archivos JSON dentro de la carpeta `data/`.

**Métodos estáticos:**

| Método | Descripción |
|--------|-------------|
| `guardar(lista_objetos, nombre_archivo)` | Serializa la lista a JSON y la escribe en `data/<archivo>` |
| `cargar(nombre_archivo)` | Lee el archivo JSON y retorna una lista de diccionarios; si no existe, retorna `[]` |
| `cargar_como(archivo, clase)` — carga el JSON y retorna una lista de objetos usando el from_dict de cada modelo |

---

### `controllers/system_controller.py` — Clase `SystemController`

Controlador principal que hereda de `ICrud` y `EstadisticasMixin`. Actúa como el cerebro del sistema.

**Inicialización:** Carga automáticamente los tres archivos JSON al instanciar.

**Métodos CRUD:**

| Método | Descripción |
|--------|-------------|
| `crear(dato)` | Detecta el tipo del objeto (`Empleado`, `TipoPermiso` o `Permiso`) y lo guarda en la lista y en JSON |
| `consultar()` | Retorna un diccionario con las tres listas (`empleados`, `tipos`, `permisos`) |
| `actualizar(cat, id, nuevos_datos)` | Busca por ID y categoría (`A`/`B`/`C`) y actualiza los campos correspondientes |
| `eliminar(cat, id)` | Filtra la lista eliminando el objeto con el ID indicado y guarda el cambio |
| `generar_id(lista)` | Retorna `max(id) + 1`, o `1` si la lista está vacía |

---

### `views/console_view.py` — Clase `ConsoleView`

Gestiona toda la interacción con el usuario a través de la terminal, con colores ANSI para mejor legibilidad.

**Utilidades visuales (funciones globales):**

| Función | Descripción |
|---------|-------------|
| `limpiar_pantalla()` | Limpia la terminal con secuencias ANSI |
| `gotoxy(x, y)` | Mueve el cursor a una posición específica |
| `color(texto, *estilos)` | Envuelve texto con colores ANSI |
| `linea(char, ancho, col)` | Imprime una línea decorativa |
| `titulo_seccion(texto)` | Título con fondo azul centrado |
| `mensaje_ok / mensaje_error / mensaje_info` | Mensajes con íconos ✔ ✘ ℹ |

**Métodos principales de `ConsoleView`:**

| Método | Descripción |
|--------|-------------|
| `mostrar_menu()` | Muestra el menú principal y retorna la opción elegida |
| `pedir_datos_empleado(existentes)` | Solicita nombre, cédula (sin duplicados) y sueldo |
| `pedir_datos_tipo_permiso()` | Solicita descripción y si es remunerado |
| `pedir_datos_solicitud(empleados, tipos)` | Solicita todos los datos de una solicitud, muestra resumen con descuento |
| `pedir_datos_actualizacion(categoria)` | Pide los nuevos datos según la categoría a actualizar |
| `mostrar_todo(datos)` | Muestra el reporte completo de empleados, tipos y solicitudes |
| `confirmar_guardado()` | Menú de confirmación (Sí/No) antes de guardar |
| `mostrar_mensaje(msg)` | Muestra un mensaje y pausa esperando ENTER |

---

### `main.py` — Punto de Entrada

Instancia `SystemController` y `ConsoleView` y ejecuta el bucle principal del sistema con un `while True` que atiende cada opción del menú.

---

## Persistencia de Datos

Los datos se almacenan en tres archivos JSON ubicados en `data/`:

**`employees.json`** — Lista de empleados:
```json
{
    "id": 6,
    "nombre": "Isaac Quispe",
    "sueldo": 30000.0,
    "cedula": "1713572137"
}
```

**`permission_types.json`** — Tipos de permiso:
```json
{
    "id": 1,
    "descripcion": "Programador, Universidad",
    "remunerado": "S"
}
```

**`permissions.json`** — Solicitudes de permiso:
```json
{
    "id": 1,
    "id_empleado": 2,
    "id_tipo_permiso": 1,
    "fecha_desde": "10/03/2024",
    "fecha_hasta": "15/03/2024",
    "tipo": "D",
    "tiempo": 5
}
```

---

## Relaciones entre Clases

```
ICrud (ABC)          EstadisticasMixin
     └──────────────────────┘
                │
        SystemController
        ┌───────┼───────┐
        │       │       │
   Empleado  TipoPermiso  Permiso
                            │
               (referencia a Empleado y TipoPermiso por ID)

ConsoleView ──── usa decoradores de core/decoradores.py
JsonManager ──── usa el método a_dic() de cada modelo
```

---

## Conceptos POO Aplicados

| Concepto | Dónde se aplica |
|----------|-----------------|
| **Encapsulamiento** | `Empleado.sueldo` con `@property` y `@setter` |
| **Herencia** | `SystemController` hereda de `ICrud` y `EstadisticasMixin` |
| **Abstracción** | Interfaz `ICrud` con métodos abstractos |
| **Polimorfismo** | `crear()` detecta el tipo del objeto con `isinstance` |
| **Decoradores** | Validaciones reutilizables en `core/decoradores.py` |
| **Mixins** | `EstadisticasMixin` agrega funcionalidad sin herencia directa de entidad |
| **Separación de responsabilidades** | Patrón MVC: modelos, vista y controlador independientes |

---

## Tecnologías Utilizadas

- **Python 3.x**
- Módulos estándar: `json`, `os`, `re`, `datetime`, `abc`
- Colores de terminal: secuencias de escape ANSI
