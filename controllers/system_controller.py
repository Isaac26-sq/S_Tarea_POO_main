from core.mixins import EstadisticasMixin, ValidationMixin, LogMixin
from core.json_manager import JsonManager
from core.interfaces import ICrud

from models.employee import Empleado
from models.permission_type import TipoPermiso
from models.permission import Permiso

from controllers.employee_controller import EmployeeController
from controllers.permission_type_controller import PermissionTypeController
from controllers.permission_controller import PermissionController


class SystemController(ICrud, EstadisticasMixin):
    

    def __init__(self):
        self._emp_ctrl   = EmployeeController()
        self._tipo_ctrl  = PermissionTypeController()
        self._perm_ctrl  = PermissionController()

   

    @property
    def empleados(self):
        return self._emp_ctrl.empleados

    @empleados.setter
    def empleados(self, value):
        self._emp_ctrl.empleados = value

    @property
    def tipos_permiso(self):
        return self._tipo_ctrl.tipos_permiso

    @tipos_permiso.setter
    def tipos_permiso(self, value):
        self._tipo_ctrl.tipos_permiso = value

    @property
    def permisos(self):
        return self._perm_ctrl.permisos

    @permisos.setter
    def permisos(self, value):
        self._perm_ctrl.permisos = value

    

    def crear(self, dato):
        if isinstance(dato, Empleado):
            self._emp_ctrl.crear(dato)
        elif isinstance(dato, TipoPermiso):
            self._tipo_ctrl.crear(dato)
        elif isinstance(dato, Permiso):
            self._perm_ctrl.crear(dato)

    def consultar(self):
        return {
            "empleados": self.empleados,
            "tipos":     self.tipos_permiso,
            "permisos":  self.permisos,
        }

    def actualizar(self, categoria, id_buscar, nuevos_datos):
        if categoria == 'A':
            self._emp_ctrl.actualizar(id_buscar=id_buscar, nuevos_datos=nuevos_datos)
        elif categoria == 'B':
            self._tipo_ctrl.actualizar(id_buscar=id_buscar, nuevos_datos=nuevos_datos)
        elif categoria == 'C':
            self._perm_ctrl.actualizar(id_buscar=id_buscar, nuevos_datos=nuevos_datos)

    def eliminar(self, categoria, id_borrar):
        if categoria == 'A':
            self._emp_ctrl.eliminar(id_borrar=id_borrar)
        elif categoria == 'B':
            self._tipo_ctrl.eliminar(id_borrar=id_borrar)
        elif categoria == 'C':
            self._perm_ctrl.eliminar(id_borrar=id_borrar)
        else:
            print(f"Categoría '{categoria}' no válida. Use A, B o C.")

    

    def generar_id(self, lista_objetos):
        if not lista_objetos:
            return 1
        return max(obj.id for obj in lista_objetos) + 1
