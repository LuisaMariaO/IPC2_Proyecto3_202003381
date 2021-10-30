import re
from aprobacion import Aprobacion


class Fecha():
    def __init__(self,fecha, dia, mes, año):
        self.fecha=fecha
        self.dia=dia
        self.mes=mes
        self.año=año
        
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

    def countNitE(self,cantidad):
        self.cantidad_emisores+=cantidad
    def countNitRe(self,cantidad):
        self.cantidad_receptores+=cantidad

    def addAprobacion(self, referencia, nit_emisor,nit_receptor,valor):

        self.correlativo+=1

        if len(str(self.correlativo)) == 1:
            codigo=self.año+self.mes+self.dia+'0000000'+str(self.correlativo)
        elif len(str(self.correlativo)) == 2:
            codigo = self.año+self.mes+self.dia+'000000'+str(self.correlativo)
        elif len(str(self.correlativo)) == 3:
            codigo = self.año+self.mes+self.dia+'00000'+str(self.correlativo)
        elif len(str(self.correlativo)) == 4:
            codigo = self.año+self.mes+self.dia+'0000'+str(self.correlativo)
        elif len(str(self.correlativo)) == 5:
            codigo = self.año+self.mes+self.dia+'000'+str(self.correlativo)
        elif len(str(self.correlativo)) == 6:
            codigo = codigo = self.año+self.mes+self.dia+'00'+str(self.correlativo)
        elif len(str(self.correlativo)) == 7:
            codigo = self.año+self.mes+self.dia+'0'+str(self.correlativo)
        elif len(str(self.correlativo)) == 8:
            codigo = self.año+self.mes+self.dia+self.correlativo
        else:
            codigo = "Error"

        self.aprobaciones.append(Aprobacion(referencia, nit_emisor,nit_receptor,codigo,valor))

    def loadAprobacion(self, referencia, nit_emisor,nit_receptor,valor,codigo):
        self.aprobaciones.append(Aprobacion(referencia, nit_emisor,nit_receptor,codigo,valor))
    
    def setAtributos(self, factura_recibidas, errores_nitemisor, errores_nitreceptor, errores_iva, errores_total, referenciasduplicadas,
        facturas_correctas,cantidadnitemisores,cantidadnitreceptores):
        self.facturas_recibidas=int(factura_recibidas)
        self.errores_nitemisor=int(errores_nitemisor)
        self.errores_nitreceptor=int(errores_nitreceptor)
        self.errores_iva=int(errores_iva)
        self.errores_total=int(errores_total)
        self.referenciasduplicadas=int(referenciasduplicadas)
        self.facturas_correctas=int(facturas_correctas)
        self.cantidad_emisores=int(cantidadnitemisores)
        self.cantidad_receptores=int(cantidadnitreceptores)

        self.correlativo=int(facturas_correctas)

