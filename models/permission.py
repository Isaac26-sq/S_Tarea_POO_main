class Permiso:
    def __init__(self, id, id_empleado, id_tipo_permiso, fecha_desde, fecha_hasta, tipo, tiempo, descuento=0.0):
        self.id              = id
        self.id_empleado     = id_empleado
        self.id_tipo_permiso = id_tipo_permiso
        self.fecha_desde     = fecha_desde
        self.fecha_hasta     = fecha_hasta
        self.tipo            = tipo
        self.tiempo          = tiempo
        self.descuento       = descuento  # monto calculado y persistido

    def calcular_descuento(self, valor_hora):
        
        if self.tipo == "H":
            monto = self.tiempo * valor_hora
        else:
            monto = self.tiempo * 8 * valor_hora
        self.descuento = round(monto, 2)
        return self.descuento

    def a_dic(self):
        return {
            "id":              self.id,
            "id_empleado":     self.id_empleado,
            "id_tipo_permiso": self.id_tipo_permiso,
            "fecha_desde":     self.fecha_desde,
            "fecha_hasta":     self.fecha_hasta,
            "tipo":            self.tipo,
            "tiempo":          self.tiempo,
            "descuento":       self.descuento,
        }

    @classmethod
    def from_dict(cls, datos):
        return cls(
            datos["id"], datos["id_empleado"], datos["id_tipo_permiso"],
            datos["fecha_desde"], datos["fecha_hasta"], datos["tipo"], datos["tiempo"],
            datos.get("descuento", 0.0),  
        )
