from django.forms import ModelForm, TextInput, Textarea, Select, NumberInput, EmailInput, DateInput, TimeInput, \
    FileInput, SelectMultiple
from .models import *


class NotaForm(ModelForm):
    class Meta:
        model = Nota
        fields = '__all__'
        widgets = {
            'nota': Textarea(attrs={'rows': 3, 'placeholder': 'Escreva uma nota...'}),
        }


class PartilhaForm(ModelForm):
    class Meta:
        model = Partilha
        fields = '__all__'
        widgets = {
            'partilha': Textarea(attrs={'rows': 3, 'placeholder': 'Escreva uma partilha...'}),
            'ficheiro': forms.FileInput(attrs={'style': 'display:none;'}),
            'imagem': forms.FileInput(attrs={'style': 'display:none;'}),
        }

# class PartilhaGrupoForm(ModelForm):
#     class Meta:
#         model = PartilhaGrupo
#         fields = '__all__'
#         widgets = {
#             'descricao': Textarea(attrs={'rows': 3, 'placeholder': 'Escreva uma partilha sobre o grupo...'}),
#             'ficheiro': forms.FileInput(attrs={'style': 'display:none;'}),
#             'imagem': forms.FileInput(attrs={'style': 'display:none;'}),
#         }



class InfoSensivelForm(ModelForm):
    class Meta:
        model = InformacaoSensivel
        fields = {'nome', 'email', 'telemovel', 'imagem'}
        widgets = {
            'nome': TextInput(attrs={'class': 'form-control', 'placeholder': 'Escreva o nome ...'}),
            'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'Escreva o email ...'}),
            'telemovel': TextInput(attrs={'class': 'form-control', 'placeholder': 'Escreva a telemovel ...'}),
            'image': FileInput(attrs={'class': 'form-control'})
        }


class CuidadorForm(ModelForm):
    opEscolaridade = (
        ("Analfabeto", "Analfabeto"),
        ("1-4", "1-4"),
        ("5-10", "5-10"),
        ("11+", "11+")
    )

    opRegime = (
        ("Online", "Online"),
        ("Presencial", "Presencial"),
        ("Misto", "Misto")
    )

    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput())
    nome = forms.CharField(max_length=100, required=True)
    sexo = forms.ChoiceField(choices=Utilizador.opSexo)
    email = forms.EmailField(max_length=100)
    telemovel = forms.CharField(max_length=20)

    class Meta:
        model = Cuidador
        widgets = {
            'nascimento': DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date',
                       'required': 'true'
                       }
            ),
        }
        fields = ['username', 'nome', 'nascimento', 'sexo', 'email', 'telemovel']


class ParticipanteForm(ModelForm):
    opEscolaridade = (
        ("Analfabeto(a)", "Analfabeto(a)"),
        ("1-4", "1-4"),
        ("5-10", "5-10"),
        ("11+", "11+")
    )
    opResidencia = (
        ("Urbana", "Urbana"),
        ("Rural", "Rural"),
    )
    opSituacaoLaboral = (
        ("Empregado(a)", "Empregado(a)"),
        ("Desempregado(a)", "Desempregado(a)"),
        ("Reformado(a)", "Reformado(a)"),
        ("Doméstica", "Doméstica"),
        ("Estudante", "Estudante"),
    )
    opSituacaoEconomica = (
        ("Muito satisfatória", "Muito satisfatória"),
        ("Satisfatória", "Satisfatória"),
        ("Pouco satisfatória", "Pouco satisfatória"),
        ("Nada satisfatória", "Nada satisfatória"),
    )
    opEstadoCivil = (
        ("Solteiro(a)", "Solteiro(a)"),
        ("Casado(a) ou a viver como tal", "Casado(a) ou a viver como tal"),
        ("Viúvo(a)", "Viúvo(a)"),
        ("Divorciado(a) ou separado(a)", "Divorciado(a) ou separado(a)"),
    )
    opAgregadoFamiliar = (
        ("Vive sozinho(a)", "Vive sozinho(a)"),
        ("Vive com o cônjuge", "Vive com o cônjuge"),
        ("Vive com os filhos", "Vive com os filhos"),
        ("Vive com terceiros", "Vive com terceiros"),
        ("Vive com o cônjuge e terceiros", "Vive com o cônjuge e terceiros"),
        ("Vive com os pais", "Vive com os pais"),
    )
    opEstadoSaude = (
        ("Muito mau", "Muito mau"),
        ("Mau", "Mau"),
        ("Nem mau nem bom", "Nem mau nem bom"),
        ("Bom", "Bom"),
        ("Muito bom", "Muito bom"),
    )

    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput())
    nome = forms.CharField(max_length=100, required=True)
    sexo = forms.ChoiceField(choices=Utilizador.opSexo)
    nacionalidade = forms.CharField(max_length=20, required=True)
    escolaridade = forms.ChoiceField(choices=opEscolaridade)
    residencia = forms.ChoiceField(choices=opResidencia)
    diagnosticos = forms.ModelMultipleChoiceField(
        queryset=Doenca.objects.all(),
        required=True,
        widget=forms.CheckboxSelectMultiple  # Use CheckboxSelectMultiple widget to allow multiple choices
    )
    referenciacao = forms.ModelChoiceField(queryset=Reference.objects.all(), required=True)
    localizacao = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(max_length=100)
    telemovel = forms.CharField(max_length=20)

    class Meta:
        model = Participante
        widgets = {
            'nascimento': DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date',
                       'required': 'true'
                       }
            ),
        }
        fields = ['username', 'nome', 'nascimento', 'sexo', 'email', 'nacionalidade', 'localizacao',
                  'escolaridade', 'referenciacao', 'residencia', 'diagnosticos', 'telemovel']


"""class CuidadorUpdateForm(ModelForm):
    class Meta:
        model = Cuidador

    fields = {'nome', 'sexo', 'idade', 'nascimento', 'nacionalidade', 'telemovel', 'email',
              'localizacao', 'image'}
    widgets = {
        'nome': TextInput(attrs={'class': 'form-control', 'placeholder': 'Escreva o nome ...'}),
        'sexo': Select(attrs={'class': 'form-control'}),
        'idade': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Escreva a idade ...'}),
        'nascimento': DateInput(
            attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Escreva a data de nascimento ...'}),
        'nacionalidade': TextInput(attrs={'class': 'form-control', 'placeholder': 'Escreva a nacionalidade ...'}),
        'telemovel': TextInput(attrs={'class': 'form-control', 'placeholder': 'Escreva a telemovel ...'}),
        'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'Escreva o email ...'}),
        'localizacao': TextInput(attrs={'class': 'form-control', 'placeholder': 'Escreva a localização ...'}),
        'image': FileInput(attrs={'class': 'form-control'})
    }
"""


# NOME, TELEMOVEL E EMAIL AGORA ESTÁ EM INFO_SENSIVEL POR ISSO O FORM NAO FUNCIONA
class ColaboradorForm(ModelForm):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput())
    nome = forms.CharField(max_length=100, required=True)
    sexo = forms.ChoiceField(choices=Utilizador.opSexo)
    email = forms.EmailField(max_length=100)
    telemovel = forms.CharField(max_length=20)

    class Meta:
        model = DinamizadorConvidado
        widgets = {
            'nascimento': DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date',
                       'required': 'true'
                       }
            ),
        }
        fields = ['username', 'password', 'nome', 'sexo', 'nascimento', 'email', 'telemovel']


class DinamizadorForm(ModelForm):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput())
    nome = forms.CharField(max_length=100, required=True)
    sexo = forms.ChoiceField(choices=Utilizador.opSexo)
    nacionalidade = forms.CharField(max_length=20, required=True)
    funcao = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    localizacao = forms.CharField(max_length=20, required=True)
    telemovel = forms.CharField(max_length=20)

    class Meta:
        model = DinamizadorConvidado
        widgets = {
            'nascimento': DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date',
                       'required': 'true'
                       }
            ),
        }
        fields = ['username', 'password', 'nome', 'sexo', 'nascimento', 'nacionalidade',
                  'localizacao', 'email', 'funcao', 'telemovel']


class MentorForm(ModelForm):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput())
    nome = forms.CharField(max_length=100, required=True)
    sexo = forms.ChoiceField(choices=Utilizador.opSexo)
    nacionalidade = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(max_length=100)
    localizacao = forms.CharField(max_length=20, required=True)
    telemovel = forms.CharField(max_length=20)

    class Meta:
        model = Mentor
        widgets = {
            'nascimento': DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date',
                       'required': 'true'
                       }
            ),
        }
        fields = ['username', 'password', 'nome', 'sexo', 'nascimento', 'nacionalidade',
                  'localizacao', 'email', 'telemovel']


class Documents_Form(ModelForm):
    class Meta:
        model = Documents
        fields = {'name', 'description', 'cuidador', 'file'}
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Escreva o nome ...'}),
            'description': TextInput(attrs={'class': 'form-control', 'placeholder': 'Escreva a nacionalidade ...'}),
            'cuidador': SelectMultiple(attrs={'class': 'form-control'}),
            'file': FileInput(attrs={'class': 'form-control'})
        }


class GrupoForm(ModelForm):
    class Meta:
        model = Grupo
        fields = '__all__'
        widgets = {
            'nome': TextInput(attrs={'class': 'form-control', 'placeholder': 'Escreva o nome do Grupo ...'}),
            'diagnostico': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Escreva o diagnostico do Grupo ...'}),
            'localizacao': TextInput(attrs={'class': 'form-control', 'placeholder': 'Escreva a Localização ...'}),
            'escolaridade': Select(attrs={'class': 'form-control'}),
            'referenciacao': Select(attrs={'class': 'form-control'}),
            'programa': Select(attrs={'class': 'form-control'}),
        }


class RespostasForm(ModelForm):
    class Meta:
        model = Resposta
        fields = '__all__'
        widgets = {
            'Respostas': Textarea(attrs={'rows': 3, 'placeholder': 'Escreva uma resposta...'}),
        }


class PresencaForm(ModelForm):
    class Meta:
        model = Presenca
        fields = '__all__'
        widgets = {
            'Presenca': Textarea(attrs={'rows': 3, 'placeholder': 'Escreva a Presenca'}),
        }



class NotaGrupoForm(ModelForm):
    class Meta:
        model = NotaGrupo
        fields = '__all__'
        widgets = {
            'notaGrupo': Textarea(attrs={'rows': 3, 'placeholder': 'Escreva uma nota sobre o grupo...'}),
        }


class SessaoDataForm(ModelForm):
    class Meta:
        model = SessaoDoGrupo
        fields = ('data',)
        widgets = {
            'data': DateInput(
                format='%d/%m/%Y %H:%M',
                attrs={'class': 'form-control', 'type': 'datetime-local',
                       'placeholder': 'Escreva a data da sessao ...',
                       'required': 'true'
                       }
            ),
        }

class RespostaForm_RespostaEscrita(ModelForm):
    class Meta:
        model = Resposta
        fields = (
            'resposta_escrita',
            # 'apontamento'
        )
        widgets = {
            'resposta_escrita': Textarea(
                attrs={'rows': 1,
                       'placeholder': '',
                       'class': 'form-control pergunta',
                       }),
            # 'apontamento': Textarea(
            #     attrs={'rows': 3, 
            #     'placeholder': 'Escreva uma nota sobre o grupo...',
            #     'class': 'form-control',
            # }),
        }

        labels = {
            'resposta_escrita': '',
        }


class RespostaForm_RespostaEscrita_Dinamizador(ModelForm):
    class Meta:
        model = Resposta
        fields = (
            'resposta_escrita',
            # 'apontamento',
            'certo',
        )
        widgets = {
            'resposta_escrita': Textarea(
                attrs={'rows': 1,
                       'placeholder': '',
                       'class': 'form-control pergunta',
                       }),
            'certo': forms.CheckboxInput(attrs={'class': 'pergunta form-check-input margin-l-5'}),
            # 'apontamento': Textarea(
            #     attrs={'rows': 3, 
            #     'placeholder': 'Escreva uma nota sobre o grupo...',
            #     'class': 'form-control',
            # }),
        }

        labels = {
            'resposta_escrita': '',
        }


class RespostaForm_RespostaSubmetida(ModelForm):
    class Meta:
        model = Resposta
        fields = (
            'resposta_submetida',
            # 'apontamento'
        )


class RespostaForm_RespostaSubmetida_Dinamizador(ModelForm):
    class Meta:
        model = Resposta
        fields = (
            'resposta_submetida',
            # 'apontamento',
            'certo'
        )
        widgets = {
            'certo': forms.CheckboxInput(attrs={'class': 'form-check-input margin-l-5'}),
            # 'apontamento': Textarea(attrs={
            #     'rows': 3, 
            #     'placeholder': 'Escreva uma nota sobre o grupo...',
            #     'class': 'form-control',
            #     }),
        }


class AvaliacaoParticipanteForm(ModelForm):
    class Meta:
        CHOICES = (
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5),
        )
        model = AvaliacaoParticipante
        fields = {'interesse', 'comunicacao', 'iniciativa', 'satisfacao', 'humor', 'eficacia_relacional'}
        widgets = {
            'interesse': forms.Select(choices=CHOICES, attrs={'class': 'avaliacao_participante'}),
            'comunicacao': forms.Select(choices=CHOICES, attrs={'class': 'avaliacao_participante'}),
            'iniciativa': forms.Select(choices=CHOICES, attrs={'class': 'avaliacao_participante'}),
            'satisfacao': forms.Select(choices=CHOICES, attrs={'class': 'avaliacao_participante'}),
            'humor': forms.Select(choices=CHOICES, attrs={'class': 'avaliacao_participante'}),
            'eficacia_relacional': forms.Select(choices=CHOICES, attrs={'class': 'avaliacao_participante'}),
        }


class AvaliacaoSessaoForm(ModelForm):
    class Meta:
        CHOICES = (
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5),
        )
        CHOICES2 = (
            ("SIM", "Sim"),
            ("NAO", "Não"),
        )
        model = AvaliacaoSessao
        fields = {'planificacao_conteudos', 'adq_conteudos', 'adq_materiais', 'adq_tempo', 'grau_dominio',
                  'necessidade_treino', 'apreciacao_global', 'tipo_treino_competencias'}
        widgets = {
            'planificacao_conteudos': forms.Select(choices=CHOICES, attrs={'class': 'avaliacao_sessao'}),
            'adq_conteudos': forms.Select(choices=CHOICES, attrs={'class': 'avaliacao_sessao'}),
            'adq_materiais': forms.Select(choices=CHOICES, attrs={'class': 'avaliacao_sessao'}),
            'adq_tempo': forms.Select(choices=CHOICES, attrs={'class': 'avaliacao_sessao'}),
            'grau_dominio': forms.Select(choices=CHOICES, attrs={'class': 'avaliacao_sessao'}),
            'necessidade_treino': forms.Select(choices=CHOICES2, attrs={'class': 'avaliacao_sessao'}),
            'apreciacao_global': forms.Select(choices=CHOICES, attrs={'class': 'avaliacao_sessao'}),
            'tipo_treino_competencias': forms.Textarea(attrs={'rows': 1, 'cols': 29, 'class': 'avaliacao_sessao'})
        }

