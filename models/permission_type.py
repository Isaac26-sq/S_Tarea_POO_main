class TipoPermiso: 
    def __init__(self, id, descripcion, remunerado):
        self.id = id 
        self.descripcion = descripcion
        self.remunerado = remunerado
        

    def a_dic(self):
        return{
            "id": self.id,
            "descripcion": self.descripcion,
            "remunerado": self.remunerado
        }

    @classmethod
    def from_dict(cls, datos):
        return cls(datos["id"], datos["descripcion"], datos["remunerado"])