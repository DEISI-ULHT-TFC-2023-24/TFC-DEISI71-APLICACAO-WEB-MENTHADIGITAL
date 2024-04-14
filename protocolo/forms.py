from django import forms
from django.forms import ModelForm

from .models import *

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class AppointmentForm(ModelForm):
    
    # ParteDoUtilizador.objects.filter() == 'MentHA-Risk'
    # request.user.groups.filter(name__in=['Avaliador','Administrador','Avaliador-Risk'])

    class Meta:
        model = ParteDoUtilizador
        fields = ('part', 'data', 'time')
        labels = {'part': 'Avaliação', 'date': 'Data', 'time':'Hora'}
        widgets = {
            'part' : forms.Select(attrs={'class': 'form-control'}),
            'data' : DateInput(attrs={'class': 'form-control'}),
            'time' : TimeInput(attrs={'class': 'form-control'}),
        }
        

class PatientForm(ModelForm):
    class Meta:
        model = Participante
        fields = '__all__'
        labels = {'part': 'Avaliação', 'date': 'Data', 'time':'Hora'}
        widgets = {
            'part' : forms.Select(attrs={'class': 'form-control'}),
            'data' : DateInput(attrs={'class': 'form-control'}),
            'time' : TimeInput(attrs={'class': 'form-control'}),
        }
class FormRisk(ModelForm):
    class Meta:
        model = Risk
        fields = '__all__'

class uploadAnswerForm(ModelForm):
    class Meta:
        model = Answer

        fields = ['text_answer', 'quotation', 'notes', 'submitted_answer']
        widgets = {
            'text_answer': forms.Textarea(attrs={'rows': 3, 'cols': 0, 'class': 'notes-area form-control'}),
            'notes': forms.Textarea(attrs={'rows': 2, 'cols': 0, 'class': 'notes-area form-control'}),
        }

        labels = {'text_answer': 'Resposta escrita (se necessário):',
                  'quotation': 'Cotação',
                  'notes': 'Apontamentos',
                  'submitted_answer': 'Submeta uma fotografia'
                  }

        def __init__(self, *args, **kwargs):
            super(uploadAnswerForm, self).__init__(*args, **kwargs)
            self.fields['submitted_answer'].required = False
            self.fields['notes'].required = False

class ParticipanteForm(ModelForm):
    opEscolaridade = (
        ("Analfabeto", "Analfabeto"),
        ("1-4", "1-4"),
        ("5-10", "5-10"),
        ("11+", "11+")
    )
    opDadosCuidador = (
        ("Cuidador", "Cuidador"),
        ("Participante", "Participante"),
        ("Familiar", "Familiar")
    )
    opTestarDoencas = (
        ("Alzheimer", "Alzheimer"),
        ("Dor de cabeça aguda", "Dor de cabeça aguda"),
        ("Dor de cabeça crónica", "Dor de cabeça crónica"),
        ("Dor de cabeça recorrente", "Dor de cabeça recorrente"),
        ("Dor de cabeça tensional", "Dor de cabeça tensional"),
        ("Enxaqueca", "Enxaqueca"),
        ("Epilepsia", "Epilepsia"),
        ("Parkinson", "Parkinson"),
        ("Outra", "Outra")
    )

    imagem = forms.ImageField()
    nome = forms.CharField(max_length=100)
    sexo = forms.ChoiceField(choices=Utilizador.opSexo)
    nacionalidade = forms.CharField(max_length=20)
    escolaridade = forms.ChoiceField(choices=opEscolaridade)
    referenciacao = forms.ModelChoiceField(queryset=Reference.objects.all(), required=True)
    localizacao = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=100)
    telemovel = forms.CharField(max_length=20)
    situacaoLaboral = forms.ChoiceField(choices=opSituacaoLaboral)
    dadosCuidador = forms.ChoiceField(choices=opDadosCuidador)
    # make testarDoencas a multiple choice field
    
    
    class Meta:
        model = Participante
        widgets = {
            'nascimento': DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date',
                       'required': 'true'
                       }
            ),
            'nrFilhos': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),
        }
        fields = ['estadoCivil', 'diagnosticos', 'escolaridade', 'imagem', 'localizacao', 
                  'nacionalidade', 'temFilhos', 'nascimento',  'nivel_gds', 'sexo', 
                  'situacaoLaboral', 'autoAvaliacaoEstadoSaude', 'nrFilhos', 'email', 
                  'referenciacao', 'residencia', 'profissaoPrincipal', 
                  'situacaoEconomica', 'telemovel', 'nome', 'agregadoFamiliar', 'dadosCuidador', 'comorbilidades', 'diagnosticoPrincipal' ]
    




class CuidadorForm(ModelForm):

    imagem = forms.ImageField()
    nome = forms.CharField(max_length=100, required=True)
    sexo = forms.ChoiceField(choices=Utilizador.opSexo)
    nacionalidade = forms.CharField(max_length=20, required=True)
    escolaridade = forms.ChoiceField(choices=opEscolaridade)
    referenciacao = forms.ModelChoiceField(queryset=Reference.objects.all(), required=True)
    localizacao = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(max_length=100)
    telemovel = forms.CharField(max_length=20)
    situacaoLaboral = forms.ChoiceField(choices=opSituacaoLaboral)
    
    motivoDependecia = forms.ChoiceField(choices=opDependencia)
    viveComParticipante = forms.ChoiceField(choices=(("Sim", "Sim"), ("Não","Não")))
    
    prestadoresCuidadosFamiliares = forms.CharField(max_length=3)
    prestadoresCuidadosAmigos = forms.CharField(max_length=3)
    prestadoresCuidadosVizinhos = forms.CharField(max_length=3)
    prestadoresCuidadosProfissionaisSAD = forms.CharField(max_length=3)
    prestadoresCuidadosProfissionaisCD = forms.CharField(max_length=3)
    prestadoresCuidadosOutros = forms.CharField(max_length=3)
    tempoCuidados_meses = forms.CharField(max_length=5)
    principalMotivoParaCuidar = forms.Textarea()
    nivelContribuicao = forms.ChoiceField(choices=opNivelContribuicao)
    periodicidadeCuidado = forms.ChoiceField(choices= opPeriodicidade)
    diaNormal = forms.Textarea()

    diaNormal30DiasDormir_minutos = forms.CharField(max_length=9)
    diaNormal30DiasTarefasWC_minutos = forms.CharField(max_length=9)
    diaNormal30DiasTarefasWC_dias = forms.CharField(max_length=3)

    diaNormal30DiasTarefasCasa_minutos = forms.CharField(max_length=9)
    diaNormal30DiasTarefasCasa_dias = forms.CharField(max_length=3)

    diaNormal30DiasSupervisao_minutos = forms.CharField(max_length=9)
    diaNormal30DiasSupervisao_dias = forms.CharField(max_length=3)

    class Meta:
        model = Cuidador
        widgets = {
            'nascimento': DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date',
                       'required': 'true'
                       }
            ),
            'nrFilhos': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),
            'diaNormal': forms.Textarea(
                attrs={'style': 'border: 1px solid #4EB4BE; border-radius: 4px; width:100%;', 'rows':'4'}
            ),
        }
        fields = ['imagem','nome','sexo','nacionalidade','escolaridade',
        'referenciacao','localizacao','email','telemovel','situacaoLaboral',
        'motivoDependecia','viveComParticipante','prestadoresCuidadosFamiliares',
        'prestadoresCuidadosAmigos','prestadoresCuidadosVizinhos','prestadoresCuidadosProfissionaisSAD',
        'prestadoresCuidadosProfissionaisCD','prestadoresCuidadosOutros','tempoCuidados_meses',
        'principalMotivoParaCuidar','nivelContribuicao','periodicidadeCuidado','diaNormal',
        'diaNormal30DiasDormir_minutos','diaNormal30DiasTarefasWC_minutos','diaNormal30DiasTarefasWC_dias',
        'diaNormal30DiasTarefasCasa_minutos','diaNormal30DiasTarefasCasa_dias',
        'diaNormal30DiasSupervisao_minutos','diaNormal30DiasSupervisao_dias',
        'estadoCivil','diagnosticos','temFilhos','nascimento','autoAvaliacaoEstadoSaude',
        'nrFilhos','residencia','profissaoPrincipal','situacaoEconomica','agregadoFamiliar', 'comorbilidades', 'diagnosticoPrincipal'
        ]
    
