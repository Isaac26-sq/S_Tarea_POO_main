import os
from models.employee import Empleado
from models.permission_type import TipoPermiso
from models.permission import Permiso
from core.decoradores import error_y_pausa, Cancelar
from views.console_view import color


def limpiar():
    os.system('cls' if os.name == 'nt' else 'clear')


class MenuController:
    def __init__(self, sistema, vista):
        self.sistema = sistema
        self.vista   = vista

    def run(self):
        while True:
            opcion = self.vista.mostrar_menu()

            acciones = {
                '1': self._registrar,
                '2': self._consultar,
                '3': self._eliminar,
                '4': self._modificar,
                '5': self._estadisticas,
                '6': self._salir,
            }

            accion = acciones.get(opcion)
            if accion:
                if accion() == "salir":
                    break
            else:
                self.vista.mostrar_mensaje("Error: Opción inválida. Elija una opción del 1 al 6.")

    

    def _registrar(self):
        while True:
            limpiar()
            print("\n¿Qué desea registrar? [A] Empleado | [B] Tipo Permiso | [C] Solicitud | [R] Regresar")
            tipo = input("Seleccione: ").upper()

            if tipo == 'R':
                break

            if tipo not in ['A', 'B', 'C']:
                self.vista.mostrar_mensaje("Error: Opción no válida. Elija A, B , C o R.")
                continue

            try:
                if tipo == 'A':
                    nom, sue, ced = self.vista.pedir_datos_empleado(self.sistema.empleados)
                    nuevo = Empleado(self.sistema.generar_id(self.sistema.empleados), nom, sue, ced)
                    if self.vista.confirmar_guardado():
                        self.sistema.crear(nuevo)
                    else:
                        self.vista.mostrar_mensaje("Registro cancelado.")

                elif tipo == 'B':
                    desc, remu = self.vista.pedir_datos_tipo_permiso()
                    nuevo = TipoPermiso(self.sistema.generar_id(self.sistema.tipos_permiso), desc, remu)
                    if self.vista.confirmar_guardado():
                        self.sistema.crear(nuevo)
                    else:
                        self.vista.mostrar_mensaje("Registro cancelado.")

                elif tipo == 'C':
                    if not self.sistema.empleados:
                        self.vista.mostrar_mensaje("No hay empleados registrados. Registre uno primero.")
                        continue
                    if not self.sistema.tipos_permiso:
                        self.vista.mostrar_mensaje("No hay tipos de permiso registrados. Registre uno primero.")
                        continue
                    id_e, id_t, d, h, t, ti = self.vista.pedir_datos_solicitud(
                        self.sistema.empleados, self.sistema.tipos_permiso
                    )
                    nuevo = Permiso(self.sistema.generar_id(self.sistema.permisos), id_e, id_t, d, h, t, ti)
                    if self.vista.confirmar_guardado():
                        self.sistema.crear(nuevo)
                    else:
                        self.vista.mostrar_mensaje("Registro cancelado.")
            except Cancelar:
                self.vista.mostrar_mensaje("Operación cancelada. Regresando al submenú.")

    def _consultar(self):
        datos = self.sistema.consultar()
        self.vista.mostrar_todo(datos)

    def _eliminar(self):
        while True:
            limpiar()
            print("\nEliminar de: [A] Empleado | [B] Tipo | [C] Solicitud | [R] Regresar")
            cat = input("Categoría: ").upper()

            if cat == 'R':
                break

            if cat not in ['A', 'B', 'C']:
                self.vista.mostrar_mensaje("Error: Opción no válida. Elija A, B , C o R.")
                continue

            try:
                limpiar()
                if cat == 'A':
                    if not self.sistema.empleados:
                        self.vista.mostrar_mensaje("No hay empleados registrados.")
                        continue
                    for e in self.sistema.empleados:
                        print(f"  ID: {e.id} | {e.nombre}")
                    ids_validos = [e.id for e in self.sistema.empleados]
                elif cat == 'B':
                    if not self.sistema.tipos_permiso:
                        self.vista.mostrar_mensaje("No hay tipos de permiso registrados.")
                        continue
                    for t in self.sistema.tipos_permiso:
                        print(f"  ID: {t.id} | {t.descripcion}")
                    ids_validos = [t.id for t in self.sistema.tipos_permiso]
                elif cat == 'C':
                    if not self.sistema.permisos:
                        self.vista.mostrar_mensaje("No hay solicitudes de permiso registradas.")
                        continue

                    for p in self.sistema.permisos:
                        emp = next((e for e in self.sistema.empleados if e.id == p.id_empleado), None)
                        nombre_emp = emp.nombre if emp else f"ID {p.id_empleado}"

                        tipo = next((t for t in self.sistema.tipos_permiso if t.id == p.id_tipo_permiso), None)
                        desc_tipo = tipo.descripcion if tipo else f"ID {p.id_tipo_permiso}"

                        print(f"  ID: {p.id} | Emp: {nombre_emp} | Tipo: {desc_tipo}")

                    ids_validos = [p.id for p in self.sistema.permisos]

                print(color("  (Escriba R para cancelar)", "\033[90m"))
                while True:
                    try:
                        id_b = int(float(self.vista.obtener_id_busqueda()))
                        if id_b in ids_validos:
                            break
                        error_y_pausa(f"Error: No existe un registro con ID {id_b}.")
                    except Cancelar:
                        raise
                    except ValueError as e:
                        self.vista.mostrar_mensaje(f"Error: {e}")

                if cat == 'A':
                    permisos_activos = [p for p in self.sistema.permisos if p.id_empleado == id_b]
                    if permisos_activos:
                        self.vista.mostrar_mensaje(
                            f"No se puede eliminar: el empleado ID {id_b} "
                            f"tiene {len(permisos_activos)} permiso(s) activo(s). "
                            "Elimine primero sus solicitudes."
                        )
                        continue

                self.sistema.eliminar(cat, id_b)
            except Cancelar:
                self.vista.mostrar_mensaje("Operación cancelada. Regresando al submenú.")

    def _modificar(self):
        while True:
            limpiar()
            print("\nModificar: [A] Empleado | [B] Tipo de Permiso | [C] Solicitud | [R] Regresar")
            cat = input("Categoría: ").upper()

            if cat == 'R':
                break

            if cat not in ['A', 'B', 'C']:
                self.vista.mostrar_mensaje("Error: Opción no válida. Elija A, B , C o R.")
                continue

            try:
                limpiar()
                if cat == 'A':
                    if not self.sistema.empleados:
                        self.vista.mostrar_mensaje("No hay empleados registrados.")
                        continue
                    for e in self.sistema.empleados:
                        print(f"  ID: {e.id} | {e.nombre}")
                    ids_validos = [e.id for e in self.sistema.empleados]
                elif cat == 'B':
                    if not self.sistema.tipos_permiso:
                        self.vista.mostrar_mensaje("No hay tipos de permiso registrados.")
                        continue
                    for t in self.sistema.tipos_permiso:
                        print(f"  ID: {t.id} | {t.descripcion}")
                    ids_validos = [t.id for t in self.sistema.tipos_permiso]
                elif cat == 'C':
                    if not self.sistema.permisos:
                        self.vista.mostrar_mensaje("No hay solicitudes registradas.")
                        continue
                    for s in self.sistema.permisos:
                        emp = next((e for e in self.sistema.empleados if e.id == s.id_empleado), None)
                        nombre_emp = emp.nombre if emp else f"ID {s.id_empleado}"

                        tipo = next((t for t in self.sistema.tipos_permiso if t.id == s.id_tipo_permiso), None)
                        desc_tipo = tipo.descripcion if tipo else f"ID {s.id_tipo_permiso}"

                        print(f"  ID: {s.id} | Emp: {nombre_emp} | Tipo: {desc_tipo} | Fecha: {s.fecha_desde}")
                    ids_validos = [s.id for s in self.sistema.permisos]

                print(color("  (Escriba R para cancelar)", "\033[90m"))
                while True:
                    try:
                        id_b = int(float(self.vista.obtener_id_actualizar()))
                        if id_b in ids_validos:
                            break
                        error_y_pausa(f"Error: No existe un registro con ID {id_b}.")
                    except Cancelar:
                        raise
                    except ValueError as e:
                        self.vista.mostrar_mensaje(f"Error: {e}")

                if cat == 'A':
                    registro = next((e for e in self.sistema.empleados if e.id == id_b), None)
                elif cat == 'B':
                    registro = next((t for t in self.sistema.tipos_permiso if t.id == id_b), None)
                elif cat == 'C':
                    registro = next((p for p in self.sistema.permisos if p.id == id_b), None)
                nuevos = self.vista.pedir_datos_actualizacion(cat, registro)
                self.sistema.actualizar(cat, id_b, nuevos)
            except Cancelar:
                self.vista.mostrar_mensaje("Operación cancelada. Regresando al submenú.")                            

    def _estadisticas(self):
        limpiar()
        if not self.sistema.empleados and not self.sistema.permisos:
            self.vista.mostrar_mensaje("No hay datos registrados para generar estadísticas.")
        else:
            self.sistema.calcular_total_empleados(self.sistema.empleados)
            if not self.sistema.permisos:
                self.vista.mostrar_mensaje("No hay solicitudes registradas para calcular tiempo y descuentos.")
            else:
                self.sistema.calcular_tiempo(self.sistema.permisos)
                self.sistema.calcular_total_permisos(self.sistema.permisos, self.sistema.tipos_permiso)
                self.sistema.calcular_descuentos(self.sistema.permisos, self.sistema.tipos_permiso, self.sistema.empleados)

    def _salir(self):
        self.vista.mostrar_mensaje("Cerrando el sistema. ¡Éxito en tu proyecto de la UNEMI!")
        return "salir"
