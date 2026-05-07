from abc import ABC, abstractmethod

class ICrud(ABC):
    @abstractmethod
    def crear(self, dato):
        pass

    @abstractmethod
    def actualizar(self, categoria, id_buscar, nuevos_datos):
        pass
    
    @abstractmethod
    def consultar(self):
        pass

    @abstractmethod
    def eliminar(self, categoria, id):
        pass