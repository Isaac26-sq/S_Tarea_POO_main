
from core.interfaces import ICrud
from core.json_manager import JsonManager
from core.mixins import ValidationMixin, LogMixin
from models.permission_type import TipoPermiso


class PermissionTypeController(ICrud, ValidationMixin, LogMixin):
    DATA_FILE = "data/permission_types.json"

    def __init__(self):
        self.db = JsonManager(PermissionTypeController.DATA_FILE)
        self.tipos_permiso = [TipoPermiso.from_dict(d) for d in self.db.load()]

   

    def _generar_id(self):
        if not self.tipos_permiso:
            return 1
        return max(t.id for t in self.tipos_permiso) + 1

    # CRUD 

    def crear(self, dato=None):
        
        print("\n=== REGISTRAR TIPO DE PERMISO ===")

        if dato is None:
            descripcion = input("Descripción del tipo de permiso: ").strip()
            remunerado = input("¿Es remunerado? (S/N): ").strip().upper()

            self.validate_not_empty(descripcion, "Descripción")

            if remunerado not in ("S", "N"):
                raise ValueError("El campo remunerado debe ser 'S' o 'N'.")

            dato = TipoPermiso(self._generar_id(), descripcion, remunerado)

        self.tipos_permiso.append(dato)
        self.db.save([t.a_dic() for t in self.tipos_permiso])
        self.log("Tipo de permiso creado correctamente")

    def consultar(self):
        
        return self.tipos_permiso

    def actualizar(self, categoria=None, id_buscar=None, nuevos_datos=None):
        
        print("\n=== ACTUALIZAR TIPO DE PERMISO ===")

        if id_buscar is None:
            id_buscar = int(input("ID del tipo de permiso a modificar: "))

        tipo = next((t for t in self.tipos_permiso if t.id == id_buscar), None)

        if not tipo:
            print(f"No se encontró un tipo de permiso con ID {id_buscar}.")
            return

        if nuevos_datos is None:
            nuevos_datos = {
                "descripcion": input("Nueva descripción: ").strip(),
                "remunerado":  input("¿Es remunerado? (S/N): ").strip().upper(),
            }

        self.validate_not_empty(nuevos_datos["descripcion"], "Descripción")
        if nuevos_datos["remunerado"] not in ("S", "N"):
            raise ValueError("El campo remunerado debe ser 'S' o 'N'.")

        tipo.descripcion = nuevos_datos["descripcion"]
        tipo.remunerado  = nuevos_datos["remunerado"]

        self.db.save([t.a_dic() for t in self.tipos_permiso])
        self.log("Tipo de permiso actualizado correctamente")

    def eliminar(self, categoria=None, id_borrar=None):
       
        print("\n=== ELIMINAR TIPO DE PERMISO ===")

        if id_borrar is None:
            id_borrar = int(input("ID del tipo de permiso a eliminar: "))

        antes = len(self.tipos_permiso)
        self.tipos_permiso = [t for t in self.tipos_permiso if t.id != id_borrar]

        if len(self.tipos_permiso) == antes:
            print(f"No se encontró un tipo de permiso con ID {id_borrar}.")
            return

        self.db.save([t.a_dic() for t in self.tipos_permiso])
        self.log(f"Tipo de permiso {id_borrar} eliminado correctamente")
