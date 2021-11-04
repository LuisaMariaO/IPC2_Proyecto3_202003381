from os import path
from django.shortcuts import render
import requests
from requests.sessions import Request

from app.forms import DateForm
from app.forms import FileForm
from app.forms import ValueForm

# Create your views here.
endpoint='http://localhost:5000/'
def home(request):
    try:
        response = requests.get(endpoint)
        return render(request,'index.html')
    except:
        print("Algo pasa con la API D:")

def carga(request):
    context={
        'content': None,
        'response': None
    }

    if request.method == 'POST':
        form=FileForm(request.POST,request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            cadenabinaria=file.read()

            xml=cadenabinaria.decode('utf-8')
            context['content'] = xml
            
            response = requests.post(endpoint+'addsolicitudes', data=cadenabinaria)
            if response.ok:
                bd = open('../BackEnd/autorizaciones.xml','r')
                salida = bd.read()
                

               

                context['response'] = salida
            else:
                context['response'] = 'Error en el servidor'

    else:
        return render(request,'carga.html')
    return render(request,'carga.html',context)

def resetdata(request):
    try:
        response = requests.delete(endpoint+'resetdata')
        
        return render(request,'index.html')
    except:
        print("Algo pasa con la API D:")

def getdata(request):
    context={
        'content': None,
       
    }
    try:
        
        response = requests.get(endpoint+'getdata')
        if response.ok:
            context['content'] = response.text
        return render(request,'consulta.html',context)
    except:
        print("Algo pasa con la API D:")
def info(request):
    try:
        response = requests.get(endpoint)
        return render(request,'info.html')
    except:
        print("Algo pasa con la API D:")

def documentacion(request):
    try:
        response = requests.get(endpoint)
        return render(request,'documentacion.html')
    except:
        print("Algo pasa con la API D:")

def resumenIVA(request):
    try:
        response = requests.get(endpoint)
        return render(request,'resumenIVA.html')
    except:
        print("Algo pasa con la API D:")

def graficarIVA(request):
    
    
    context = {
        'data': [None],
        'fecha': None
    }
    
    if request.method == 'GET':
        form = DateForm(request.GET)
    try:  
        if form.is_valid():
            json_data = form.cleaned_data
            fecha=str(json_data['date'])
            lfecha=fecha.split('-')
            context['fecha'] = lfecha[2]+'/'+lfecha[1]+'/'+lfecha[0]
            response = requests.get(endpoint + 'resumeniva/'+lfecha[2]+'/'+lfecha[1]+'/'+lfecha[0]) #'/resumeniva/<dia>/<mes>/<anio>
            data = response.json()
            context['data'] = data
            
        else:
            form = DateForm()      
    except:
        print('Algo anda mal con la API D:')
    return render(request, 'resumenIVA.html',context)

def graficaFechas(request): 
      
    
    context = {
        'data': [None],
        'rango': None
    }
    
    if request.method == 'GET':
        
        form= ValueForm(request.GET)

    try:  
        if form.is_valid():
            
            json_data = form.cleaned_data
            
            fecha1=str(json_data['fecha1'])
            lfecha1=fecha1.split('-')

            fecha2=str(json_data['fecha2'])
            lfecha2=fecha2.split('-')

            valor=str(json_data['valor'])
            if valor=='Total':
                valorp='total'
            else:
                valorp='SIva'

            context['rango'] = lfecha1[2]+'/'+lfecha1[1]+'/'+lfecha1[0]+'-'+lfecha2[2]+'/'+lfecha2[1]+'/'+lfecha2[0]+' Tipo de valor: '+valor
            response = requests.get(endpoint + 'resumenfecha/'+lfecha1[2]+'/'+lfecha1[1]+'/'+lfecha1[0]+'='+lfecha2[2]+'/'+lfecha2[1]+'/'+lfecha2[0]+'/'+valorp) #resumenfecha/09/01/2021=09/05/2021/total
            data = response.json()
            context['data'] = data
            
        else:
            form = ValueForm()      
    except:
        print('Algo anda mal con la API D:')
    return render(request, 'resumenFechas.html',context)  
    


