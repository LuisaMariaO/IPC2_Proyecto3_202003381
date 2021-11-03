


class Nit():
    def __init__(self,nit):
        self.nit=nit
        self.ivaemitido=0
        self.ivarecibido=0
       
    def searchNit(self,nit):
        if nit==self.nit:
            return True
        else:
            return False
    def countIvaRecibido(self,iva):
        self.ivarecibido+=iva
    def countIvaEmitido(self,iva):
        self.ivaemitido+=iva