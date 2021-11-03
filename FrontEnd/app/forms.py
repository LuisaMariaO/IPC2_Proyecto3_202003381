from django import forms

class FileForm(forms.Form):
    file = forms.FileField(label="file")

class DateForm(forms.Form):
   date = forms.Field(label="date")
   
 
