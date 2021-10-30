from flask import Flask, request
from flask.json import jsonify
from manage import Manager
from xml.etree import ElementTree as ET
import re

app = Flask(__name__)

manager = Manager()
@app.route('/')
def index():
    return "API is working jus fine! uwu"

@app.route('/addsolicitudes', methods=['POST'])
def add_solicitudes():

    #try:
    manager.getDatabase()
    #except:
        #pass
    xml = str(request.data.decode('utf-8'))
    meses31=['1','3','5','7','8','10','12']
    meses30=['4','5','9','11']

    root = ET.fromstring(xml)
    for dte in root.iter('DTE'):
        tiempo=dte.find('TIEMPO').text
        referencia=dte.find('REFERENCIA').text
        nite=dte.find('NIT_EMISOR').text
        nitre=dte.find('NIT_RECEPTOR').text
        valor=dte.find('VALOR').text
        iva=dte.find('IVA').text
        total=dte.find('TOTAL').text
        
        #Verifico el formato correcto del tag tiempo
        
   
        #Encuentro la fecha
        patronfecha=re.compile('[0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9]')
        fecha=patronfecha.search(tiempo)
        fecha=fecha.group(0)
        #Encuentro la hora

        lfecha=fecha.split('/')
        

        patronreferencia=re.compile('(\w){1,40}')
        nreferencia=patronreferencia.search(referencia)
        nreferencia=nreferencia.group(0)

        #Verifico que los valores numéricos cumplan con dos decimales
        patrondecimales=re.compile('(\d)+\.(\d)(\d)')

        nvalor=patrondecimales.search(valor)
        nvalor=nvalor.group(0)
        niva=patrondecimales.search(iva)
        niva=niva.group(0)
        ntotal=patrondecimales.search(total)
        ntotal=ntotal.group(0)

        #Verifico que el día, mes y año tengan sentido
        dia=lfecha[0]
        mes=lfecha[1]
        año=lfecha[2]

        if mes in meses31:
            if int(dia)<=31:
                pass
            else:
                dia=None
        elif mes in meses30:
            if int(dia)<=30:
                pass
            else:
                dia=None
        elif mes == '2':
            if int(dia)<=29 and int(año)%4 == 0:
                pass
            elif int(dia)<=28:
                pass
            else:
                dia=None
        else:
            mes=0


 
        if dia !=None and mes != None:
            manager.add_solicitud(fecha,lfecha[0],lfecha[1],lfecha[2],nreferencia,nite,nitre,nvalor,niva,ntotal)
    manager.verify_solicitudes()
    manager.llenarXML()
        

 
    return jsonify({'ok':True, 'msg':'Archivo XML cargado correctamente :D'}), 200

if __name__=='__main__':
    app.run(host='localhost',debug=True)