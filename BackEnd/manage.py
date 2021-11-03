from os import path
from re import S
from xml.etree import ElementTree as ET
from solicitud import Solicitud
from fecha import Fecha
from nit import Nit
from fechagrafica import Fechagrafica
from peticion import Peticion
class Manager():
    def __init__(self):
        self.solicitudes = []
        self.fechas=[]
        self.auxfechas=[]
        self.nofacturas=0
        self.auxreferencias = []

        self.peticiones=[]



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
            self.fechas.append(Fecha(self.solicitudes[0].fecha,self.solicitudes[0].dia, self.solicitudes[0].mes, self.solicitudes[0].año))
        #Por cada solicitud, busco la fecha en el arreglo de fechas, para guardar la fecha una sola vez
        for solicitud in self.solicitudes:
            found=False
            for fecha in self.fechas:
                if  fecha.searchFecha(solicitud.fecha):
                    found=True
            if not found:
                self.fechas.append(Fecha(solicitud.fecha,solicitud.dia,solicitud.mes, solicitud.año))
            #Lleno una lista auxiliar de referencias para verificar repeticiones después
            self.auxreferencias.append(solicitud.referencia)

        self.fechas.sort(key = lambda f: f.fecha) #about 9 - 6.1 = 3 secs
        
        #Por cada solicitud, si coincide con una fecha en la lista de fechas, sumo uno al contador de facturas
        for solicitud in self.solicitudes:
            for fecha in self.fechas:
                if fecha.searchFecha(solicitud.fecha):
                    fecha.countFacturas()
        

        #Verificando las referencias, si se encuentra una referencia duplicada, se desactiva la solicitud
        '''
        for solicitud in self.solicitudes:
            for fecha in self.fechas:
                if fecha.verifyReferencia(solicitud.referencia):
                    fecha.countReferenciasDuplicadas()
                    solicitud.desactivar()'''
        
                    

        
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

                if fecha.searchFecha(solicitud.fecha) and fecha.verifyReferencia(solicitud.referencia): #Revisa la repeticion de referencia
                    found = True
                    fecha.countReferenciasDuplicadas()
                    solicitud.desactivar()
                
            if not found and solicitud.activa:
                for fecha in self.fechas:
                    if fecha.fecha == solicitud.fecha:
                        fecha.addAprobacion(solicitud.referencia, solicitud.nit_emisor, solicitud.nit_receptor, solicitud.valor)
                        
        #Buscando en las facturas correctas el número de nit diferentes


        for fecha in self.fechas:
            nitemisores=[]
            nitreceptores=[]
            #Cuento los nit emisores
            for aprobacion in fecha.aprobaciones:
                if aprobacion.nit_emisor in nitemisores:
                    pass
                    #fecha.countNitE()
                else:
                    nitemisores.append(aprobacion.nit_emisor)
                    
            #Cuento los nit receptores
                if aprobacion.nit_receptor in nitreceptores:
                    pass
                    #fecha.countNitRe()
                else:
                    nitreceptores.append(aprobacion.nit_receptor)

            fecha.countNitE(len(nitemisores))
            fecha.countNitRe(len(nitreceptores))
                
        

        
                        
                
                    


        return True
    def llenarXML(self):
        xml=open('autorizaciones.xml','w')
        body='<LISTAAUTORIZACIONES>'
        for fecha in self.fechas:
            body+='\n\t<AUTORIZACION>'
            body+='\n\t<FECHA>'+fecha.fecha+'</FECHA>'
            body+='\n\t<FACTURAS_RECIBIDAS>'+str(fecha.facturas_recibidas)+'</FACTURAS_RECIBIDAS>'
            body+='\n\t<ERRORES>'
            body+='\n\t\t<NIT_EMISOR>'+str(fecha.errores_nitemisor)+'</NIT_EMISOR>'
            body+='\n\t\t<NIT_RECEPTOR>'+str(fecha.errores_nitreceptor)+'</NIT_RECEPTOR>'
            body+='\n\t\t<IVA>'+str(fecha.errores_iva)+'</IVA>'
            body+='\n\t\t<TOTAL>'+str(fecha.errores_total)+'</TOTAL>'
            body+='\n\t\t<REFERENCIA_DUPLICADA>'+str(fecha.referenciasduplicadas)+'</REFERENCIA_DUPLICADA>'
            body+='\n\t</ERRORES>'
            body+='\n\t<FACTURAS_CORRECTAS>'+str(len(fecha.aprobaciones))+'</FACTURAS_CORRECTAS>'
            body+='\n\t<CANTIDAD_EMISORES>'+str(fecha.cantidad_emisores)+'</CANTIDAD_EMISORES>'
            body+='\n\t<CANTIDAD_RECEPTORES>'+str(fecha.cantidad_receptores)+'</CANTIDAD_RECEPTORES>'
            body+='\n\t<LISTADO_AUTORIZACIONES>'
            for aprobacion in fecha.aprobaciones:
                body+='\n\t\t<APROBACION>'
                body+='\n\t\t\t<NIT_EMISOR ref="'+aprobacion.referencia+'">'+aprobacion.nit_emisor+'</NIT_EMISOR>'
                body+='\n\t\t\t<CODIGO_APROBACION>'+aprobacion.codigo+'</CODIGO_APROBACION>'
                body+='\n\t\t\t<NIT_RECEPTOR>'+aprobacion.nit_receptor+'</NIT_RECEPTOR>'
                body+='\n\t\t\t<VALOR>'+aprobacion.valor+'</VALOR>'
                body+='\n\t\t</APROBACION>'
            body+='\n\t\t<TOTAL_APROBACIONES>'+str(len(fecha.aprobaciones))+'</TOTAL_APROBACIONES>'
            body+='\n\t</LISTADO_AUTORIZACIONES>'


            body+='\n\t</AUTORIZACION>'



           
        body+='\n</LISTAAUTORIZACIONES>'
        xml.write(body)
        xml.close()

        #Regresando las listas iniciadas a su valor inicial
        self.fechas.clear()
        self.solicitudes.clear()
        self.nofacturas=0
        self.auxfechas=0

    def getDatabase(self):
        self.fechas.clear()
        tree = ET.parse('autorizaciones.xml')
        root = tree.getroot()
        
        for autorizacion in root.iter('AUTORIZACION'):
            fecha=autorizacion.find('FECHA').text
            lfecha=fecha.split('/')
            self.fechas.append(Fecha(fecha,lfecha[0],lfecha[1],lfecha[2]))
     
        for fecha in self.fechas:
            for autorizacion in root.iter('AUTORIZACION'):
                if fecha.searchFecha(autorizacion.find('FECHA').text):
                    facturas_recibidas=autorizacion.find('FACTURAS_RECIBIDAS').text
                    for error in autorizacion.iter('ERRORES'):
                        error_nit_emisor=error.find('NIT_EMISOR').text
                        error_nit_receptor=error.find('NIT_RECEPTOR').text
                        error_iva=error.find('IVA').text
                        error_total=error.find('TOTAL').text
                        referenciasduplicadas=error.find('REFERENCIA_DUPLICADA').text
                    facturascorrectas=autorizacion.find('FACTURAS_CORRECTAS').text
                    cantidademisores=autorizacion.find('CANTIDAD_EMISORES').text
                    cantidadreceptores=autorizacion.find('CANTIDAD_RECEPTORES').text
                    fecha.setAtributos(facturas_recibidas,error_nit_emisor,error_nit_receptor,error_iva,error_total,
                    referenciasduplicadas,facturascorrectas,0,0)

                    for lista in autorizacion.iter('LISTADO_AUTORIZACIONES'):
                        for aprobacion in lista.iter('APROBACION'):
                            nitemisor=aprobacion.find('NIT_EMISOR').text
                            referencia=aprobacion.find('NIT_EMISOR').attrib['ref']
                            codigo=aprobacion.find('CODIGO_APROBACION').text
                            nitreceptor=aprobacion.find('NIT_RECEPTOR').text
                            valor=aprobacion.find('VALOR').text
                            fecha.loadAprobacion(referencia,nitemisor,nitreceptor,valor,codigo)
    def resumeniva(self,dia,mes,año):
        nits=[]
        nonits=[]
        
        for fecha in self.fechas:
            
            if dia==fecha.dia and mes==fecha.mes and año==fecha.año:
                #Me aseguro de no repetir nits
                for aprobacion in fecha.aprobaciones:
                    if aprobacion.nit_emisor not in nonits:
                        nonits.append(aprobacion.nit_emisor)
                    if aprobacion.nit_receptor not in nonits:
                        nonits.append(aprobacion.nit_receptor)
                
                #Creo una lista de nits (objeto)        
                for nit in nonits:
                    nits.append(Nit(nit))
                for aprobacion in fecha.aprobaciones:
                    for nit in nits:
       
                        if nit.nit == aprobacion.nit_emisor:
                            
                            iva=float(aprobacion.valor)*0.12
                            nit.countIvaEmitido(iva)
                        if nit.nit == aprobacion.nit_receptor:
                            iva=float(aprobacion.valor)*0.12
                            nit.countIvaRecibido(iva)

           
        
        json = []    
        for n in nits:
            nit = {
                'nit': n.nit,
                'iva_recibido': n.ivarecibido,
                'iva_emitido': n.ivaemitido
            }
            json.append(nit)
        return json
    
    def resumenfecha(self,diai,mesi,anioi,diaf,mesf,aniof,param):
        fechasgrafica=[]
        for fecha in self.fechas:
            
            if fecha.dia>=diai and fecha.dia<=diaf and fecha.mes>=mesi and fecha.mes<=mesf and fecha.año>=anioi and fecha.año<=aniof:
                fechasgrafica.append(Fechagrafica(fecha.fecha))

        
        if param=='total':
            for f in fechasgrafica:
                for fecha in self.fechas:
                    if f.fecha==fecha.fecha:
                        for ap in fecha.aprobaciones:
                            total=float(ap.valor)+(float(ap.valor)*0.12)
                            f.sumTotal(total)
        elif param=='SIva':
             for f in fechasgrafica:
                for fecha in self.fechas:
                    if f.fecha==fecha.fecha:
                        for ap in fecha.aprobaciones:
                            valor=float(ap.valor)
                            f.sumSIva(valor)



                    
            
                
           
        
        json = []

        if param=='total':
            for f in fechasgrafica:
                fecha={
                    'fecha': f.fecha,
                    'total':f.vtotal
                }
                json.append(fecha)  

        elif param=='SIva':
            for f in fechasgrafica:
                fecha={
                    'fecha': f.fecha,
                    'vsinIVA':f.vsiniva
                }
                json.append(fecha)  

  
        return json

    def addPeticion(self,nombre,tipo,fecha,hora):
        self.peticiones.append(Peticion(nombre,tipo,fecha,hora))
   
    def reporte(self):
        
        json = []
        for p in self.peticiones:
            
            peticion={
                'ruta':p.nombre,
                'tipo':p.tipo,
                'fecha':p.fecha,
                'hora':p.hora
            }
            json.append(peticion)
        
        return json



        



        
