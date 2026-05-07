# Paquete de controllers: uno por cada entidad + fachada + menú.
from .employee_controller import EmployeeController
from .permission_type_controller import PermissionTypeController
from .permission_controller import PermissionController
from .system_controller import SystemController
from .menu_controller import MenuController

__all__ = [
    "EmployeeController",
    "PermissionTypeController",
    "PermissionController",
    "SystemController",
    "MenuController",
]
