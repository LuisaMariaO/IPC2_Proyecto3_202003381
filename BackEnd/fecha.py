import re
from aprobacion import Aprobacion


class Fecha():
    def __init__(self,fecha):
        self.fecha=fecha
        
        #Otros atribibutos que puede tener una fecha

        #Errores
        self.facturas_recibidas=0
        self.errores_nitemisor=0
        self.errores_nitreceptor=0
        self.errores_iva=0
        self.errores_total=0
        self.referenciasduplicadas=0

        self.facturas_correctas=0
        self.cantidad_emisores=0
        self.cantidad_receptores=0

        self.aprobaciones=[]

        self.correlativo=0

    def countFacturas(self):
        self.facturas_recibidas+=1

    def searchFecha(self,fecha):
        if fecha == self.fecha:
            return True
        else:
            return False

    def countReferenciasDuplicadas(self):
        self.referenciasduplicadas+=1

    def verifyReferencia(self,referencia):
        for aprobacion in self.aprobaciones:
            try:
                if aprobacion.referencia == referencia:
                    return True
            except:
                pass
        return False
    def countErrorNitE(self):
        self.errores_nitemisor+=1
    def countErrorNitR(self):
        self.errores_nitreceptor+=1
    def countErrorIva(self):
        self.errores_iva+=1
    def countErrorTotal(self):
        self.errores_total+=1

    def addAprobacion(self, referencia, nit_emisor,nit_receptor,valor):

        self.correlativo+=1

        if len(str(self.correlativo)) == 1:
            codigo='0000000'+str(self.correlativo)
        elif len(str(self.correlativo)) == 2:
            codigo = '000000'+str(self.correlativo)
        elif len(str(self.correlativo)) == 3:
            codigo = '00000'+str(self.correlativo)
        elif len(str(self.correlativo)) == 4:
            codigo = '0000'+str(self.correlativo)
        elif len(str(self.correlativo)) == 5:
            codigo = '000'+str(self.correlativo)
        elif len(str(self.correlativo)) == 6:
            codigo = codigo = '00'+str(self.correlativo)
        elif len(str(self.correlativo)) == 7:
            codigo = '0'+str(self.correlativo)
        elif len(str(self.correlativo)) == 8:
            codigo = self.correlativo
        else:
            codigo = "Error"

        self.aprobaciones.append(Aprobacion(referencia, nit_emisor,nit_receptor,codigo,valor))
