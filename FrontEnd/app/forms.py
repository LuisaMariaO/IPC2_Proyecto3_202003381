from django import forms

class FileForm(forms.Form):
    file = forms.FileField(label="file")

class DateForm(forms.Form):
   date = forms.Field(label="date")
   

class ValueForm(forms.Form):
    fecha1=forms.DateField(label="fecha1")
    fecha2=forms.DateField(label="fecha1")
    valor = forms.ComboField(label="valor",fields=[forms.CharField(max_length=10)])
