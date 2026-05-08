
from core.interfaces import ICrud
from core.json_manager import JsonManager
from core.mixins import ValidationMixin, LogMixin
from models.permission import Permiso


class PermissionController(ICrud, ValidationMixin, LogMixin):
    DATA_FILE       = "data/permissions.json"
    EMPLOYEES_FILE  = "data/employees.json"
    PERM_TYPES_FILE = "data/permission_types.json"

    def __init__(self):
        self.db       = JsonManager(PermissionController.DATA_FILE)
        self.db_emp   = JsonManager(PermissionController.EMPLOYEES_FILE)
        self.db_tipos = JsonManager(PermissionController.PERM_TYPES_FILE)

        self.permisos       = [Permiso.from_dict(d) for d in self.db.load()]
        self._empleados_raw = self.db_emp.load()
        self._tipos_raw     = self.db_tipos.load()

   

    def _generar_id(self):
        if not self.permisos:
            return 1
        return max(p.id for p in self.permisos) + 1

    def _id_empleado_valido(self, id_emp):
        return any(e["id"] == id_emp for e in self._empleados_raw)

    def _id_tipo_valido(self, id_tipo):
        return any(t["id"] == id_tipo for t in self._tipos_raw)

    def _get_valor_hora(self, id_emp):
        
        emp = next((e for e in self._empleados_raw if e["id"] == id_emp), None)
        return emp["sueldo"] / 240 if emp else 0.0

    def _tipo_es_remunerado(self, id_tipo):
        tipo = next((t for t in self._tipos_raw if t["id"] == id_tipo), None)
        return tipo["remunerado"] == "S" if tipo else True

    # CRUD 

    def crear(self, dato=None):
        
        print("\n=== REGISTRAR SOLICITUD DE PERMISO ===")

        if dato is None:
            id_empleado     = int(input("ID del empleado: "))
            id_tipo_permiso = int(input("ID del tipo de permiso: "))
            fecha_desde     = input("Fecha desde (DD/MM/YYYY): ").strip()
            fecha_hasta     = input("Fecha hasta (DD/MM/YYYY): ").strip()
            tipo            = input("Tipo de tiempo (D=Días / H=Horas): ").strip().upper()
            tiempo          = float(input("Cantidad de tiempo: "))

            if not self._id_empleado_valido(id_empleado):
                raise ValueError(f"No existe un empleado con ID {id_empleado}.")
            if not self._id_tipo_valido(id_tipo_permiso):
                raise ValueError(f"No existe un tipo de permiso con ID {id_tipo_permiso}.")
            self.validate_not_empty(fecha_desde, "Fecha desde")
            self.validate_not_empty(fecha_hasta, "Fecha hasta")
            if tipo not in ("D", "H"):
                raise ValueError("El tipo debe ser 'D' (días) o 'H' (horas).")
            self.validate_positive_number(tiempo, "Tiempo")

            dato = Permiso(self._generar_id(), id_empleado, id_tipo_permiso,
                           fecha_desde, fecha_hasta, tipo, tiempo)

       
        if not self._tipo_es_remunerado(dato.id_tipo_permiso):
            dato.calcular_descuento(self._get_valor_hora(dato.id_empleado))

        self.permisos.append(dato)
        self.db.save([p.a_dic() for p in self.permisos])
        self.log("Solicitud de permiso creada correctamente")

    def consultar(self):
        return self.permisos

    def actualizar(self, categoria=None, id_buscar=None, nuevos_datos=None):
        print("\n=== ACTUALIZAR SOLICITUD DE PERMISO ===")

        if id_buscar is None:
            id_buscar = int(input("ID de la solicitud a modificar: "))

        solicitud = next((p for p in self.permisos if p.id == id_buscar), None)
        if not solicitud:
            print(f"No se encontró una solicitud con ID {id_buscar}.")
            return

        if nuevos_datos is None:
            nuevos_datos = {
                "fecha_desde": input("Nueva fecha desde (DD/MM/YYYY): ").strip(),
                "fecha_hasta": input("Nueva fecha hasta (DD/MM/YYYY): ").strip(),
                "tipo":        input("Tipo de tiempo (D=Días / H=Horas): ").strip().upper(),
                "tiempo":      float(input("Nueva cantidad de tiempo: ")),
            }

        self.validate_not_empty(nuevos_datos["fecha_desde"], "Fecha desde")
        self.validate_not_empty(nuevos_datos["fecha_hasta"], "Fecha hasta")
        if nuevos_datos["tipo"] not in ("D", "H"):
            raise ValueError("El tipo debe ser 'D' (días) o 'H' (horas).")
        self.validate_positive_number(nuevos_datos["tiempo"], "Tiempo")

        solicitud.fecha_desde = nuevos_datos["fecha_desde"]
        solicitud.fecha_hasta = nuevos_datos["fecha_hasta"]
        solicitud.tipo        = nuevos_datos["tipo"]
        solicitud.tiempo      = nuevos_datos["tiempo"]

        
        if not self._tipo_es_remunerado(solicitud.id_tipo_permiso):
            solicitud.calcular_descuento(self._get_valor_hora(solicitud.id_empleado))
        else:
            solicitud.descuento = 0.0

        self.db.save([p.a_dic() for p in self.permisos])
        self.log("Solicitud de permiso actualizada correctamente")

    def eliminar(self, categoria=None, id_borrar=None):
        print("\n=== ELIMINAR SOLICITUD DE PERMISO ===")

        if id_borrar is None:
            id_borrar = int(input("ID de la solicitud a eliminar: "))

        antes = len(self.permisos)
        self.permisos = [p for p in self.permisos if p.id != id_borrar]

        if len(self.permisos) == antes:
            print(f"No se encontró una solicitud con ID {id_borrar}.")
            return

        self.db.save([p.a_dic() for p in self.permisos])
        self.log(f"Solicitud {id_borrar} eliminada correctamente")
