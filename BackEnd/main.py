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
    xml = str(request.data.decode('utf-8'))
 

    root = ET.fromstring(xml)
    for dte in root.iter('DTE'):
        tiempo=dte.find('TIEMPO').text
        referencia=dte.find('REFERENCIA').text
        nite=dte.find('NIT_EMISOR').text
        nitre=dte.find('NIT_RECEPTOR').text
        valor=dte.find('VALOR').text
        iva=dte.find('IVA').text
        total=dte.find('TOTAL').text
        
   
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

 
        
        manager.add_solicitud(fecha,lfecha[0],lfecha[1],lfecha[2],nreferencia,nite,nitre,nvalor,niva,ntotal)
    manager.verify_solicitudes()
        

 
    return jsonify({'ok':True, 'msg':'Archivo XML cargado correctamente :D'}), 200

if __name__=='__main__':
    app.run(host='localhost',debug=True)