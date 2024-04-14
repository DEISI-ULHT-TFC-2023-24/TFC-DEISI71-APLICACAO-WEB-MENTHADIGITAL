from django import forms
from django.forms import ModelForm

from .models import Contacto

# Create your models here.
class ContactoForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['telefone'].widget.attrs.update({'class': 'form-control'})
        self.fields['assunto'].widget.attrs.update({'class': 'form-control'})
        self.fields['distrito'].widget.attrs.update({'class': 'form-control'})
        self.fields['referenciacao'].widget.attrs.update({'class': 'form-control'})
        self.fields['mensagem'].widget.attrs.update({'class': 'form-control', 'rows':5, 'placeholder':'Insira a sua mensagem...'})
    
    
    class Meta:
        model = Contacto
        fields = '__all__'

        labels = { 'referenciacao': 'Instituição Referenciadora'}

