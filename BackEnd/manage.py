from re import S
from solicitud import Solicitud
from fecha import Fecha
class Manager():
    def __init__(self):
        self.solicitudes = []
        self.fechas=[]
        self.auxfechas=[]
        self.nofacturas=0
        self.auxreferencias = []



    def add_solicitud(self,fecha,dia,mes,año,referencia, nit_emisor, nit_receptor, valor, iva, total):
        nit_emisor=nit_emisor.replace(' ','')
        nit_receptor=nit_receptor.replace(' ','')
        self.solicitudes.append(Solicitud(fecha,dia,mes,año,referencia, nit_emisor, nit_receptor, valor, iva, total))
        return True

    def verify_solicitudes(self):
        
        
        

    #Primero llenar las fechas, verificar si existe primero. 
    #Luego de llenarlas, con la lista de solicitudes ir sumando el número de facturas.

        #Lleno la primera posición del arreglo de fechas, en caso de que esté vacía todavía
        if len(self.fechas)==0:
            self.fechas.append(Fecha(self.solicitudes[0].fecha))
        #Por cada solicitud, busco la fecha en el arreglo de fechas, pare guardar la fecha una sola vez
        for solicitud in self.solicitudes:
            found=False
            for fecha in self.fechas:
                if  fecha.searchFecha(solicitud.fecha):
                    found=True
            if not found:
                self.fechas.append(Fecha(solicitud.fecha))
            #Lleno una lista auxiliar de referencias para verificar repeticiones después
            self.auxreferencias.append(solicitud.referencia)
        
        #Por cada solicitud, si coincide con una fecha en la lista de fechas, sumo uno al contador de facturas
        for solicitud in self.solicitudes:
            for fecha in self.fechas:
                if fecha.searchFecha(solicitud.fecha):
                    fecha.countFacturas()
        

        #Verificando las referencias, si se encuentra una referencia duplicada, se desactiva la solicitud
        for solicitud in self.solicitudes:
            for fecha in self.fechas:
                if fecha.verifyReferencia(solicitud.referencia):
                    fecha.countReferenciasDuplicadas()
                    solicitud.desactivar()
        
                    

        
        #Verificando los nit emisores de las solicitudes que no se han desactivado
    
        for solicitud in self.solicitudes:
            sumatoria=0
            
            nitemisor=list(solicitud.nit_emisor)
            nitemisor.reverse()
            if len(nitemisor)<=20:
                
            
                for i in range (1,len(nitemisor)):

                    sumatoria+=int(nitemisor[i])*(i+1)
                    
                modulo = sumatoria % 11
    
                resta = 11-modulo
                k = resta % 11
                #print(k)
    
                if k < 10 and str(k) == nitemisor[0]:
                    #print("Nit aceptado :3")
                    pass
                else:
                    for fecha in self.fechas:
                        if fecha.searchFecha(solicitud.fecha):
                            fecha.countErrorNitE()
                            solicitud.desactivar()
            else:
                solicitud.desactivar()
            

      #Verificando los nit receptores
    
        for solicitud in self.solicitudes:
            sumatoria=0
           
            nitreceptor=list(solicitud.nit_receptor)
            nitreceptor.reverse()
            if len(nitreceptor)<=20:
                
            
                for i in range (1,len(nitreceptor)):

                    sumatoria+=int(nitreceptor[i])*(i+1)
                    #print(sumatoria)
                modulo = sumatoria % 11
                #print(sumatoria)
                resta = 11-modulo
                k = resta % 11
                #print(k)

                if k < 10 and str(k) == nitreceptor[0]:
                    #print("Nit aceptado:D")
                    pass
                else:
                    for fecha in self.fechas:
                        if fecha.searchFecha(solicitud.fecha):
                            fecha.countErrorNitR()
                            solicitud.desactivar()
            else:
                solicitud.desactivar()
        
        

        #Verificando los montos
        for solicitud in self.solicitudes:
            #verificando el valor
            if solicitud.valor is not None:
                #Verificando el cálculo del iva
                iva = float(solicitud.valor)*0.12
                iva=round(iva,2)
                
                
                iva=("{0:.2f}".format(iva))
                

                if str(iva) == solicitud.iva:
                    pass
                else:
                    for fecha in self.fechas:
                        if fecha.searchFecha(solicitud.fecha):
                            fecha.countErrorIva()
                            solicitud.desactivar()
                #Verificando el cálculo del total
                total = round(float(solicitud.valor)+float(solicitud.iva),2)
                total=("{0:.2f}".format(total))
                if total == solicitud.total:
                    pass
                else:
                    for fecha in self.fechas:
                        if fecha.searchFecha(solicitud.fecha):
                            fecha.countErrorTotal()
                            solicitud.desactivar()

        #Haciendo el último filtro de referencias repetidas y guardando las solicitudes que quedaron activas
        for solicitud in self.solicitudes:
            found=False
            for fecha in self.fechas:
                if fecha.verifyReferencia(solicitud.referencia):
                    found = True
                    fecha.countReferenciasDuplicadas()
                    solicitud.desactivar()
                if not found and solicitud.activa:
                    for fecha in self.fechas:
                        if fecha.fecha == solicitud.fecha:
                            fecha.addAprobacion(solicitud.referencia, solicitud.nit_emisor, solicitud.nit_receptor, solicitud.valor)
                            

                    
                        


                    


        for fecha in self.fechas:
            print(fecha.fecha," Facturas recibidas ",fecha.facturas_recibidas, " Errores Nitemisor ", fecha.errores_nitemisor, " Errores Nitreceptor ",fecha.errores_nitreceptor," Errores iva ",fecha.errores_iva," Errores total ",fecha.errores_total)
            for aprobacion in fecha.aprobaciones:
                print(aprobacion.codigo)
        return True