class Empleado: 
    def __init__(self, id, nombre, sueldo, cedula ):
        self.id = id 
        self.nombre = nombre
        self.sueldo = sueldo
        self.cedula = cedula
        self.valor_hora = self.sueldo / 240

    @property
    def sueldo(self):
        return self.__sueldo
    
    @sueldo.setter
    def sueldo(self, valor):
        if valor < 0:
            raise ValueError("El sueldo no puede ser negativo.")
        self.__sueldo = valor
       
        self.valor_hora = self.__sueldo / 240

    def a_dic(self):
        return{
            "id": self.id,
            "nombre": self.nombre,
            "sueldo": self.sueldo,
            "cedula": self.cedula  
        }

    @classmethod
    def from_dict(cls, datos):
        return cls(datos["id"], datos["nombre"], datos["sueldo"], datos["cedula"])