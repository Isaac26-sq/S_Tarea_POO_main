import re
import datetime

_ROJO  = "\033[91m"
_GRIS  = "\033[90m"
_RESET = "\033[0m"

_SUBIR   = "\033[1A"
_LIMPIAR = "\033[2K"


def error_y_pausa(mensaje):
    print(f"{_ROJO}  {mensaje}{_RESET}")
    input(f"{_GRIS}  Presione ENTER para continuar...{_RESET}")

    print(f"{_SUBIR}{_LIMPIAR}", end="", flush=True)

    print(f"{_SUBIR}{_LIMPIAR}", end="", flush=True)

    print(f"{_SUBIR}{_LIMPIAR}", end="", flush=True)


class Cancelar(Exception):
    pass


def validar_nombre(funcion):
    def wrapper(*args, **kwargs):
        while True:
            validar = funcion(*args, **kwargs).strip()
            if validar.upper() == 'R':
                raise Cancelar()
            patron = r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$"
            partes = validar.split()
            if validar and re.match(patron, validar) and len(partes) >= 2:
                return validar.title()
            error_y_pausa("Error: Ingrese al menos un nombre y un apellido (solo letras).")
    return wrapper


def validar_texto(funcion):
    def wrapper(*args, **kwargs):
        while True:
            validar = funcion(*args, **kwargs).strip()
            if validar.upper() == 'R':
                raise Cancelar()
            if validar and any(c.isalpha() for c in validar):
                return validar
            error_y_pausa("Error: La descripción no puede estar vacía ni contener solo números o símbolos.")
    return wrapper


def validar_numero(funcion):
    def wrapper(*args, **kwargs):
        while True:
            try:
                valor_str = funcion(*args, **kwargs).strip()
                if valor_str.upper() == 'R':
                    raise Cancelar()
                valor = float(valor_str)
                if valor > 0:
                    return valor
                error_y_pausa("Error: El valor debe ser mayor a 0. Intente de nuevo")
            except Cancelar:
                raise
            except:
                error_y_pausa("Error: Debe ingresar un valor númerico válido.")
    return wrapper

def validar_fecha(funcion):
    def wrapper(*args, **kwargs):
        while True:
            validar = funcion(*args, **kwargs).strip()
            if validar.upper() == 'R':
                raise Cancelar()
            try:
                fecha = datetime.datetime.strptime(validar, '%d/%m/%Y').date()
                if fecha > datetime.date.today():
                    error_y_pausa("Error: La fecha no puede sobre pasar a la fecha actual.")
                    continue
                return validar
            except ValueError:
                error_y_pausa("Error: Formato inválido. Use DD/MM/YYYY y verifique que el día y mes sean lógicos.")
    return wrapper

def validar_d_h(funcion):
    def wrapper(*args, **kwargs):
        while True:
            validar = funcion(*args, **kwargs).strip().upper()
            if validar == 'R':
                raise Cancelar()
            if validar in ['D', 'H']:
                return validar
            error_y_pausa("Error: Entrada inválida. Ingrese 'D' (Dias) o 'H' (Horas).")
    return wrapper


def validar_s_n(funcion):
    def wrapper(*args, **kwargs):
        while True:
            validar = funcion(*args, **kwargs).strip().upper()
            if validar == 'R':
                raise Cancelar()
            if validar in ['S', 'N']:
                return validar
            error_y_pausa("Error: Entrada inválida. Ingrese 'S' (Si) o 'N' (No).")
    return wrapper

def validar_cedula(funcion):
    def wrapper(*args, **kwargs):
        while True:
            validar = funcion(*args, **kwargs).strip()
            if validar.upper() == 'R':
                raise Cancelar()
            if not (validar.isdigit() and len(validar) == 10):
                error_y_pausa("Error: Cédula inválida. Debe contener exactamente 10 números (sin letras).")
                continue
            
            provincia = int(validar[:2])
            if not (0 < provincia <= 24):
                error_y_pausa("Error: Código de provincia inválido.")
                continue

            digitos = [int(d) for d in validar]
            verificador = digitos.pop() 
            coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
            suma = 0

            for i in range(len(digitos)):
                valor = digitos[i] * coeficientes[i]
                if valor >= 10:
                    valor -= 9
                suma += valor
            
            residuo = suma % 10
            resultado = 0 if residuo == 0 else 10 - residuo

            if resultado == verificador:
                return validar
            error_y_pausa("Error: Cédula falsa (Módulo 10 fallido).")
    return wrapper     


                
         
           


        
        
        