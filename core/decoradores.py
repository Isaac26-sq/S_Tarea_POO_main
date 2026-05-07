import re
import datetime
def validar_nombre(funcion):
    def wrapper(*args, **kwargs):

        while True:
            validar = funcion(*args, **kwargs).strip()
            patron = r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$"
            if validar and re.match(patron, validar): 
                return validar
            print("Error: El nombre debe contener solo letras y no estar vacío.")
    return wrapper
    

def validar_texto(funcion):
    def wrapper(*args, **kwargs):

        while True:
            validar = funcion(*args, **kwargs).strip()
            
            if validar and any(c.isalpha() for c in validar):
                return validar
            print("Error: La descripción no puede estar vacía ni contener solo números o símbolos.")
    return wrapper


def validar_numero(funcion):
    def wrapper(*args, **kwargs):
        while True: 
            try:
                valor_str = funcion(*args, **kwargs).strip()
                valor = float(valor_str)
                if valor > 0:
                    return valor
                print("Error: El valor debe ser mayor a 0. Intente de nuevo")
            except:
                print("Error: Debe ingresar un valor númerico válido.")
    return wrapper
    
def validar_fecha(funcion):
    def wrapper(*args, **kwargs):
        while True:
            validar = funcion(*args, **kwargs).strip()
            try:
                datetime.datetime.strptime(validar, '%d/%m/%Y')
                return validar
            except ValueError:
                print("Error: Formato de fecha invalidad. Use DD/MM/YYYY.")
                print("Asegúrese que el día y mes sean lógicos (ej: mes 1 al 12).")
    return wrapper

def validar_d_h(funcion):
    def wrapper(*args, **kwargs):
        while True:
            validar = funcion(*args, **kwargs).strip().upper()
            if validar in ['D', 'H']:
                return validar
            print("Error: Entrada inválida. Ingrese 'D' (Dias) o 'H' (Horas).")
    return wrapper
                     

def validar_s_n(funcion):
    def wrapper(*args, **kwargs):
        while True:
            validar = funcion(*args, **kwargs).strip().upper()
            if validar in ['S', 'N']:
                return validar
            print("Error: Entrada inválida. Ingrese 'S' (Si) o 'N' (No).")
    return wrapper 

def validar_cedula(funcion):
    def wrapper(*args, **kwargs):
        while True:
            validar = funcion(*args, **kwargs).strip() 
            if not (validar.isdigit() and len(validar) == 10): 
                print("Error: Cédula inválida. Debe contener exactamente 10 números (sin letras).")  
                continue
            
            provincia = int(validar[:2])
            if not (0 < provincia <= 24):
                print("Error: Código de provincia inválido.")
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
            print("Error: Cédula falsa (Módulo 10 fallido).")
    return wrapper     


                
         
           


        
        
        