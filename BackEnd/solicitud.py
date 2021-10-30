class Solicitud():
    def __init__(self,fecha,dia,mes,año, referencia, nit_emisor, nit_resceptor, valor, iva, total):
        self.fecha=fecha
        self.dia=dia
        self.mes=mes
        self.año=año

        self.activa=True

        self.referencia=referencia
        self.nit_emisor=nit_emisor
        self.nit_receptor=nit_resceptor
        self.valor=valor
        self.iva=iva
        self.total=total

    
    def getSolicitud(self):
        return self
    def desactivar(self):
        self.activa=False