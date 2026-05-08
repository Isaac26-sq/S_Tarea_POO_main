from core.decoradores import validar_nombre, validar_texto, validar_numero, validar_fecha, validar_d_h, validar_s_n, validar_cedula, error_y_pausa
from models.permission import Permiso as _Permiso
from datetime import datetime
import os

def limpiar_pantalla():
    
    os.system('cls' if os.name == 'nt' else 'clear')


class Color:
    RESET      = "\033[0m"
    BOLD       = "\033[1m"

  
    BLANCO     = "\033[97m"
    AMARILLO   = "\033[93m"
    CYAN       = "\033[96m"
    VERDE      = "\033[92m"
    ROJO       = "\033[91m"
    MAGENTA    = "\033[95m"
    AZUL       = "\033[94m"
    GRIS       = "\033[90m"

   
    FONDO_AZUL     = "\033[44m"
    FONDO_VERDE    = "\033[42m"
    FONDO_ROJO     = "\033[41m"
    FONDO_CYAN     = "\033[46m"
    FONDO_MAGENTA  = "\033[45m"
    FONDO_NEGRO    = "\033[40m"
    FONDO_AMARILLO = "\033[43m"

def color(texto, *estilos):
    
    return "".join(estilos) + str(texto) + Color.RESET

def linea(caracter="═", ancho=60, col=None):
    
    linea_str = caracter * ancho
    if col:
        print(color(linea_str, col))
    else:
        print(linea_str)

def titulo_seccion(texto, ancho=60):
    
    pad = " " * ((ancho - len(texto)) // 2)
    print(color(f"{pad}{texto}{pad}", Color.FONDO_AZUL, Color.BLANCO, Color.BOLD))

def subtitulo(texto, col=Color.CYAN):
    
    print(color(f"\n  ── {texto} ──", col, Color.BOLD))

def mensaje_ok(texto):
    print(color(f"\n  ✔  {texto}", Color.VERDE, Color.BOLD))

def mensaje_error(texto):
    print(color(f"\n  ✘  {texto}", Color.ROJO, Color.BOLD))

def mensaje_info(texto):
    print(color(f"\n  ℹ  {texto}", Color.AMARILLO))

def pausa():
    input(color("\n  Presione ENTER para continuar...", Color.GRIS))




class ConsoleView:

    def mostrar_menu(self):
        limpiar_pantalla()
        ancho = 50

        
        linea("═", ancho, Color.AZUL)
        titulo_seccion("SISTEMA DE GESTIÓN RRHH - UNEMI", ancho)
        linea("═", ancho, Color.AZUL)

        
        opciones = [
            ("1", "Registrar Nuevo Empleado",      Color.VERDE),
            ("2", "Consultar Registros",            Color.CYAN),
            ("3", "Eliminar Registro por ID",       Color.ROJO),
            ("4", "Modificar Registro",             Color.AMARILLO),
            ("5", "Ver Estadísticas y Reportes",    Color.MAGENTA),
            ("6", "Salir",                          Color.GRIS),
        ]
        for num, desc, col in opciones:
            print(f"  {color(f'[{num}]', col, Color.BOLD)}  {color(desc, Color.BLANCO)}")

        linea("═", ancho, Color.AZUL)
        return input(color("  Elija una opción (1-6): ", Color.AMARILLO, Color.BOLD))

   

    @validar_nombre
    def obtener_nombre(self):
        return input(color("  Nombre y Apellido: ", Color.CYAN))
            
    @validar_numero
    def obtener_sueldo(self):
        return input(color("  Sueldo mensual ($): ", Color.CYAN))

    @validar_cedula
    def obtener_cedula(self):
        return input(color("  Cédula: ", Color.CYAN))

    def pedir_datos_empleado(self, empleado_existentes):
        limpiar_pantalla()
        linea("─", 50, Color.VERDE)
        titulo_seccion("REGISTRO DE EMPLEADO", 50)
        linea("─", 50, Color.VERDE)

        nombre = self.obtener_nombre()
        while True:
            cedula = self.obtener_cedula()
            duplicado = any(e.cedula == cedula for e in empleado_existentes)
            if duplicado:
                mensaje_error(f"La cédula {cedula} ya está registrada en el sistema.")
            else:
                break
        sueldo = self.obtener_sueldo()

        return nombre, sueldo, cedula

    def confirmar_guardado(self):
        print(color("\n  ¿Desea guardar?", Color.AMARILLO, Color.BOLD))
        print(f"  {color('1', Color.VERDE, Color.BOLD)}  Sí")
        print(f"  {color('2', Color.ROJO,  Color.BOLD)}  No")
        while True:
            opcion = input(color("  Seleccione: ", Color.AMARILLO))
            if opcion in ['1', '2']:
                return opcion == '1'
            
            error_y_pausa("Error: Opción inválida. Ingrese 1 o 2.")

   

    @validar_texto
    def obtener_descripcion_permiso(self):
        return input(color("  Descripción (Ej: Vacaciones): ", Color.CYAN))

    @validar_s_n
    def obtener_s_n(self):
        return input(color("  ¿Es remunerado? (S/N): ", Color.CYAN)).upper()

    def pedir_datos_tipo_permiso(self):
        limpiar_pantalla()
        linea("─", 50, Color.MAGENTA)
        titulo_seccion("REGISTRO DE TIPO DE PERMISO", 50)
        linea("─", 50, Color.MAGENTA)

        desc = self.obtener_descripcion_permiso()
        remu = self.obtener_s_n()
        return desc, remu

   

    @validar_numero
    def obtener_id_empleado(self):
        return input(color("  ID del Empleado: ", Color.CYAN))

    @validar_numero
    def obtener_id_tipo(self):
        return input(color("  ID del Tipo de Permiso: ", Color.CYAN))

    @validar_numero
    def obtener_cantidad_tiempo(self):
        return input(color("  Cantidad (Número): ", Color.CYAN))

    @validar_fecha
    def obtener_fecha_inicio(self):
        return input(color("  Fecha Inicio (DD/MM/AAAA): ", Color.CYAN))

    @validar_fecha
    def obtener_fecha_fin(self):
        return input(color("  Fecha Fin (DD/MM/AAAA): ", Color.CYAN))

    @validar_d_h
    def obtener_d_h(self):
        return input(color("  ¿En Días o Horas? (D/H): ", Color.CYAN))

    def pedir_datos_solicitud(self, empleados, tipos_permiso):
        limpiar_pantalla()
        linea("─", 50, Color.CYAN)
        titulo_seccion("NUEVA SOLICITUD DE PERMISO", 50)
        linea("─", 50, Color.CYAN)

        subtitulo("EMPLEADOS DISPONIBLES", Color.VERDE)
        for e in empleados:
            print(color(f"    ID: {e.id}", Color.AMARILLO, Color.BOLD) +
                  color(f"  |  {e.nombre}", Color.BLANCO))

        ids_empleados = [e.id for e in empleados]
        while True:
            id_emp = int(self.obtener_id_empleado())
            if id_emp in ids_empleados:
                break
            error_y_pausa(f"No existe un empleado con ID {id_emp}. Elija uno de los disponibles.")

        subtitulo("TIPOS DE PERMISO DISPONIBLES", Color.VERDE)
        for t in tipos_permiso:
            remu_txt = color("Remunerado", Color.VERDE) if t.remunerado == 'S' else color("No remunerado", Color.ROJO)
            print(color(f"    ID: {t.id}", Color.AMARILLO, Color.BOLD) +
                  color(f"  |  {t.descripcion}  ", Color.BLANCO) +
                  f"[{remu_txt}]")

        ids_tipos = [t.id for t in tipos_permiso]
        while True:
            id_tipo = int(self.obtener_id_tipo())
            if id_tipo in ids_tipos:
                break
            error_y_pausa(f"No existe un tipo de permiso con ID {id_tipo}. Elija uno de los disponibles.")

        desde = self.obtener_fecha_inicio()
        while True:
            hasta = self.obtener_fecha_fin()
            if datetime.strptime(hasta, '%d/%m/%Y') >= datetime.strptime(desde, '%d/%m/%Y'):
                break
            error_y_pausa("La fecha de fin no puede ser anterior a la fecha de inicio.")

        tipo  = self.obtener_d_h()
        tiempo = int(self.obtener_cantidad_tiempo())

        tipo_obj   = next((t for t in tipos_permiso if t.id == id_tipo), None)
        remunerado = tipo_obj.remunerado if tipo_obj else "N"
        emp_obj    = next((e for e in empleados if e.id == id_emp), None)

        
        _permiso_tmp = _Permiso(0, id_emp, id_tipo, desde, hasta, tipo, tiempo)

        linea("─", 50, Color.AMARILLO)
        titulo_seccion("RESUMEN DE SOLICITUD", 50)
        linea("─", 50, Color.AMARILLO)
        remu_str = color("Sí", Color.VERDE, Color.BOLD) if remunerado == 'S' else color("No", Color.ROJO, Color.BOLD)
        print(color("  ¿Remunerado? ", Color.BLANCO) + remu_str)
        if remunerado == 'N' and emp_obj:
            descuento = _permiso_tmp.calcular_descuento(emp_obj.valor_hora)
            print(color(f"  Descuento aplicado: ", Color.BLANCO) +
                  color(f"${descuento:.2f}", Color.ROJO, Color.BOLD))
        else:
            print(color("  Descuento aplicado: ", Color.BLANCO) +
                  color("$0.00", Color.VERDE, Color.BOLD))

        return id_emp, id_tipo, desde, hasta, tipo, tiempo

    

    @validar_numero
    def obtener_id_actualizar(self):
        return input(color("  Ingrese el ID a Actualizar: ", Color.AMARILLO))

    @validar_numero
    def obtener_id_busqueda(self):
        return input(color("  Ingrese el ID a eliminar: ", Color.ROJO))

    def mostrar_todo(self, datos):
        limpiar_pantalla()
        linea("═", 60, Color.AZUL)
        titulo_seccion("REPORTE GENERAL DE REGISTROS", 60)
        linea("═", 60, Color.AZUL)

        
        subtitulo("EMPLEADOS", Color.VERDE)
        if not datos["empleados"]:
            mensaje_info("Sin empleados registrados.")
        else:
            for e in datos["empleados"]:
                print(color(f"  ID: {e.id}", Color.AMARILLO, Color.BOLD) +
                      color(f"  |  {e.nombre:<25}", Color.BLANCO) +
                      color(f"  Valor/Hora: ${e.valor_hora:.2f}", Color.CYAN))

        
        subtitulo("TIPOS DE PERMISOS", Color.MAGENTA)
        if not datos["tipos"]:
            mensaje_info("Sin tipos de permiso registrados.")
        else:
            for t in datos["tipos"]:
                remu_txt = color("S", Color.VERDE, Color.BOLD) if t.remunerado == 'S' else color("N", Color.ROJO, Color.BOLD)
                print(color(f"  ID: {t.id}", Color.AMARILLO, Color.BOLD) +
                      color(f"  |  {t.descripcion:<25}", Color.BLANCO) +
                      "  Remunerado: " + remu_txt)

       
        subtitulo("SOLICITUDES DE PERMISO", Color.CYAN)
        if not datos["permisos"]:
            mensaje_info("Sin solicitudes registradas.")
        else:
            for p in datos["permisos"]:
                emp_obj = next((e for e in datos["empleados"] if e.id == p.id_empleado), None)
                nombre_emp = emp_obj.nombre if emp_obj else f"ID: {p.id_empleado}"

                tipo_obj = next((t for t in datos["tipos"] if t.id == p.id_tipo_permiso), None)
                desc_tipo = tipo_obj.descripcion if tipo_obj else f"ID: {p.id_tipo_permiso}"

                tipo_txt = color("Días", Color.AZUL) if p.tipo == 'D' else color("Horas", Color.MAGENTA)
                
                print(color(f"  ID: {p.id}", Color.AMARILLO, Color.BOLD) +
                      color(f"  |  Emp: {nombre_emp:<20}", Color.BLANCO) +
                      color(f"  |  Tipo: {desc_tipo:<15}", Color.BLANCO) +
                      f"  |  {p.tiempo} " + tipo_txt)

        linea("═", 60, Color.AZUL)
        pausa()

    def pedir_datos_actualizacion(self, categoria):
        if categoria == 'A':
            limpiar_pantalla()
            linea("─", 50, Color.AMARILLO)
            titulo_seccion("ACTUALIZAR EMPLEADO", 50)
            linea("─", 50, Color.AMARILLO)
            nombre = self.obtener_nombre()
            sueldo = self.obtener_sueldo()
            return {"nombre": nombre, "sueldo": sueldo}

        elif categoria == 'B':
            limpiar_pantalla()
            linea("─", 50, Color.AMARILLO)
            titulo_seccion("ACTUALIZAR TIPO DE PERMISO", 50)
            linea("─", 50, Color.AMARILLO)
            desc = self.obtener_descripcion_permiso()
            remu = self.obtener_s_n().upper()
            return {"descripcion": desc, "remunerado": remu}

        elif categoria == 'C':
            limpiar_pantalla()
            linea("─", 50, Color.AMARILLO)
            titulo_seccion("ACTUALIZAR SOLICITUD", 50)
            linea("─", 50, Color.AMARILLO)
            desde = self.obtener_fecha_inicio()
            while True:
                hasta = self.obtener_fecha_fin()
                if datetime.strptime(hasta, '%d/%m/%Y') >= datetime.strptime(desde, '%d/%m/%Y'):
                    break
                mensaje_error("La fecha de fin no puede ser anterior a la fecha de inicio.")
            tipo   = self.obtener_d_h()
            tiempo = int(self.obtener_cantidad_tiempo())
            return {"fecha_desde": desde, "fecha_hasta": hasta, "tipo": tipo, "tiempo": tiempo}
        else:
            mensaje_error(f"Categoría de actualización '{categoria}' no reconocida.")
            return {}
    
    def mostrar_mensaje(self, mensaje):
        print(color(f"\n  {mensaje}", Color.AMARILLO))
        pausa()
