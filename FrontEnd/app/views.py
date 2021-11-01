from django.shortcuts import render
import requests
from requests.sessions import Request
from app.forms import FileForm

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
