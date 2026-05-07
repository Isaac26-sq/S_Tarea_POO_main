# Mixin de validaciones reutilizables para modelos y controladores.
class ValidationMixin:

    @staticmethod
    def validate_not_empty(value, field_name):
        
        if not str(value).strip():
            raise ValueError(f"{field_name} no puede estar vacío")

    @staticmethod
    def validate_positive_number(value, field_name):
        
        if value <= 0:
            raise ValueError(f"{field_name} debe ser mayor a 0")



class LogMixin:
    LOG_PREFIX = "[LOG]"

    def log(self, message):
        print(f"{LogMixin.LOG_PREFIX}: {message}")



class EstadisticasMixin:

    def calcular_total_empleados(self, lista_empleados):
        total = len(lista_empleados)
        print(f"\033[96m\n  ── ESTADÍSTICAS ──────────────────────────\033[0m")
        print(f"\033[93m  Total de empleados en nómina: \033[97m{total}\033[0m")
        return total

    def calcular_total_permisos(self, lista_permisos, lista_tipos):
        total = len(lista_permisos)
        remunerados = sum(
            1 for p in lista_permisos
            if next((t for t in lista_tipos if t.id == p.id_tipo_permiso), None) and
               next(t for t in lista_tipos if t.id == p.id_tipo_permiso).remunerado == 'S'
        )
        no_remunerados = total - remunerados

        print(f"\033[93m  Total de permisos:     \033[97m{total}\033[0m")
        print(f"\033[92m  Remunerados:           \033[97m{remunerados}\033[0m")
        print(f"\033[91m  No remunerados:        \033[97m{no_remunerados}\033[0m")

    def calcular_tiempo(self, lista_permisos):
        total_dias  = sum(p.tiempo for p in lista_permisos if p.tipo == "D")
        total_horas = sum(p.tiempo for p in lista_permisos if p.tipo == "H")
        print(f"\033[96m\n  ── REPORTE DE TIEMPO ─────────────────────\033[0m")
        print(f"\033[93m  Total acumulado: \033[97m{total_dias} Días  y  {total_horas} Horas\033[0m")

    def calcular_descuentos(self, lista_permisos, lista_tipos, lista_empleados):
        """Usa Permiso.calcular_descuento() como única fuente de verdad del cálculo."""
        total_descuento = 0

        for permiso in lista_permisos:
            tipo = next((t for t in lista_tipos if t.id == permiso.id_tipo_permiso), None)
            if tipo and tipo.remunerado == "N":
                emp = next((e for e in lista_empleados if e.id == permiso.id_empleado), None)
                if emp:
                    total_descuento += permiso.calcular_descuento(emp.valor_hora)

        print(f"\033[96m\n  ── REPORTE FINANCIERO ────────────────────\033[0m")
        print(f"\033[91m  Monto total a descontar: \033[97m${total_descuento:.2f}\033[0m")
        print(f"\033[96m  ──────────────────────────────────────────\033[0m")
        input(f"\033[90m\n  Presione ENTER para continuar...\033[0m")
        return total_descuento
