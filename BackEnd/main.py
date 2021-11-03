from flask import Flask, request
from flask.json import jsonify
from manage import Manager
from xml.etree import ElementTree as ET
import re
from datetime import datetime
import xmltodict
import json
from peticion import Peticion




app = Flask(__name__)

manager = Manager()
@app.route('/')
def index():
    return "API is working jus fine! uwu"

@app.route('/addsolicitudes', methods=['POST'])
def add_solicitudes():
    now= datetime.now()
    manager.addPeticion('/addsolicitudes','POST',now.date(),now.time())
    try:
        manager.getDatabase()
    except:
        pass
    xml = str(request.data.decode('utf-8'))
    root = ET.fromstring(xml)

    meses31=['1','3','5','7','8','10','12']
    meses30=['4','5','9','11']
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

       
        #Verifico la lógica de la estructura de la fecha, si es válida, se almacena toda su información
        try:
            datetime.strptime(fecha, '%d/%m/%Y')
            lfecha=fecha.split('/')
            manager.add_solicitud(fecha,lfecha[0],lfecha[1],lfecha[2],nreferencia,nite,nitre,nvalor,niva,ntotal)
        except:
            pass


  

        
    try:
        manager.verify_solicitudes()
        manager.llenarXML()
        return jsonify({'ok':True, 'msg':'Archivo XML cargado correctamente :D'}), 200
    except:
        return jsonify({'ok':True, 'msg':'Algo salió mal en la carga :('}), 400

@app.route('/getdata', methods=['GET'])
def getdata(): 
    now= datetime.now()
    manager.addPeticion('/getdata','GET',str(now.date()),str(now.time()))
    print(now.date(),now.time())
    try:
        #Convierto la base xml a json
        with open('autorizaciones.xml', 'r') as xmlfile:
            db = xmltodict.parse(xmlfile.read())
            
            jsonstring=json.dumps(db)
            xmlfile.close()

            file=open('autorizaciones.xml','r')
            xml=file.read()
            file.close()
            
           
        return xml, 200
    except:
        return jsonify({'ok':True, 'msg':'No hay autorizaciones para mostrar'}), 400

@app.route('/resetdata',methods=['DELETE'])
def resetdata():
    now= datetime.now()
    manager.addPeticion('/resetdata','DELETE',str(now.date()),str(now.time()))
    try:
        db=open('autorizaciones.xml','w')
        db.write('')
        db.close()
        return jsonify({'ok':True, 'msg':'Base de datos eliminada'}), 200
    except:
        return jsonify({'ok':True, 'msg':'No hay registros para borrar'}), 400

@app.route('/resumeniva/<dia>/<mes>/<anio>', methods=['GET'])
def resumeniva(dia,mes,anio):
    now= datetime.now()
    manager.addPeticion('/resumeniva/'+dia+'/'+mes+'/'+anio,'GET',str(now.date()),str(now.time()))
    try:
        manager.getDatabase()
        res = manager.resumeniva(dia,mes,anio)
        return jsonify(res), 200
    except:
        return jsonify({'ok':True, 'msg':'No es posible generar el resumen'}), 400
        
@app.route('/resumenfecha/<diai>/<mesi>/<anioi>=<diaf>/<mesf>/<aniof>/<param>',methods=['GET'])
def resumenfecha(diai,mesi,anioi,diaf,mesf,aniof,param):
    now= datetime.now()
    manager.addPeticion('/resumenfecha/'+diai+'/'+mesi+'/'+anioi+'='+diaf+'/'+mesf+'/'+aniof+'/'+param,'GET',str(now.date()),str(now.time()))
    try:
        manager.getDatabase()
        res = manager.resumenfecha(diai,mesi,anioi,diaf,mesf,aniof,param)
        return jsonify(res), 200
    except:
        return jsonify({'ok':True, 'msg':'No es posible generar el resumen'}), 400

@app.route('/reporte',methods=['GET'])
def reporte():
    try:
        res = manager.reporte()
        return jsonify(res),200
    except:
        return jsonify({'ok':True, 'msg':'No es posible generar el reporte'}), 400


    

                
        

 
    

if __name__=='__main__':
    app.run(host='localhost',debug=True)