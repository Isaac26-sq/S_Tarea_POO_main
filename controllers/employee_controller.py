
from core.interfaces import ICrud
from core.json_manager import JsonManager
from core.mixins import ValidationMixin, LogMixin
from models.employee import Empleado


class EmployeeController(ICrud, ValidationMixin, LogMixin):
    DATA_FILE = "data/employees.json"

    def __init__(self):
        self.db = JsonManager(EmployeeController.DATA_FILE)
        self.empleados = [Empleado.from_dict(d) for d in self.db.load()]

    

    def _generar_id(self):
        if not self.empleados:
            return 1
        return max(e.id for e in self.empleados) + 1

    def _cedula_existe(self, cedula):
        return any(e.cedula == cedula for e in self.empleados)

    # CRUD 

    def crear(self, dato=None):
        
        print("\n=== REGISTRAR EMPLEADO ===")

        if dato is None:
            nombre = input("Nombre completo: ").strip()
            cedula = input("Cédula: ").strip()
            sueldo = float(input("Sueldo mensual: "))

            self.validate_not_empty(nombre, "Nombre")
            self.validate_not_empty(cedula, "Cédula")
            self.validate_positive_number(sueldo, "Sueldo")

            if self._cedula_existe(cedula):
                raise ValueError(f"Ya existe un empleado con cédula {cedula}.")

            dato = Empleado(self._generar_id(), nombre, sueldo, cedula)

        self.empleados.append(dato)
        self.db.save([e.a_dic() for e in self.empleados])
        self.log("Empleado creado correctamente")

    def consultar(self):
        
        return self.empleados

    def actualizar(self, categoria=None, id_buscar=None, nuevos_datos=None):
       
        print("\n=== ACTUALIZAR EMPLEADO ===")

        if id_buscar is None:
            id_buscar = int(input("ID del empleado a modificar: "))

        empleado = next((e for e in self.empleados if e.id == id_buscar), None)

        if not empleado:
            print(f"No se encontró un empleado con ID {id_buscar}.")
            return

        if nuevos_datos is None:
            nuevos_datos = {
                "nombre": input("Nuevo nombre: ").strip(),
                "sueldo": float(input("Nuevo sueldo: ")),
            }

        self.validate_not_empty(nuevos_datos["nombre"], "Nombre")
        self.validate_positive_number(nuevos_datos["sueldo"], "Sueldo")

        empleado.nombre = nuevos_datos["nombre"]
        empleado.sueldo = nuevos_datos["sueldo"]

        self.db.save([e.a_dic() for e in self.empleados])
        self.log("Empleado actualizado correctamente")

    def eliminar(self, categoria=None, id_borrar=None):
        
        print("\n=== ELIMINAR EMPLEADO ===")

        if id_borrar is None:
            id_borrar = int(input("ID del empleado a eliminar: "))

        antes = len(self.empleados)
        self.empleados = [e for e in self.empleados if e.id != id_borrar]

        if len(self.empleados) == antes:
            print(f"No se encontró un empleado con ID {id_borrar}.")
            return

        self.db.save([e.a_dic() for e in self.empleados])
        self.log(f"Empleado {id_borrar} eliminado correctamente")
