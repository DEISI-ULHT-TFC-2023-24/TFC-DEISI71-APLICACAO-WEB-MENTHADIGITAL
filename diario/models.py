from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django import forms
from django.conf import settings
import math
from django.core.validators import MaxValueValidator, MinValueValidator
from django.http import HttpResponse

from .functions import *

def valida_str(string):
    if string == None or len(string) == 0 or string == "0":
        return "Sem informação"
    else:
        return string
    
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
opDependencia = (
    ("Demência/Doença Neurocognitiva (cognitiva adquirida)", "Demência/Doença Neurocognitiva (cognitiva adquirida)"),
    ("Deficiência Intelectual (cognitiva congénita)", "Deficiência Intelectual (cognitiva congénita)"),
    ("Doença do foro psicológico (emocional/psiquiátrica)", "Doença do foro psicológico (emocional/psiquiátrica)")

)

opPeriodicidade = (
    ("Sempre, excepto em situações esporádicas", "Sempre, excepto em situações esporádicas"),
    ("Durante a semana (normalmente de 2ª feira a 6ª feira)", "Durante a semana (normalmente de 2ª feira a 6ª feira)"),
    ("Fins de semana (ou período entre os 2-3 dias /semana)", "Fins de semana (ou período entre os 2-3 dias /semana)"),
    ("Rotativo (a meses)", "Rotativo (a meses)"),
    ("Durante o final da tarde e/ou noite", "Durante o final da tarde e/ou noite"),
    ("Pontualmente (1 ou 2 vezes por mês)", "Pontualmente (1 ou 2 vezes por mês)"),
    ("Período de férias", "Período de férias"),
    ("Outro", "Outro"),
)
opNivelContribuicao = (
    (f"1%-20%", f"1%-20%"),
    (f"21%-40%", f"21%-40%"),
    (f"41%-60%", f"41%-60%"),
    (f"61%-80%", f"61%-80%"),
    (f"81%-100%", f"81%-100%"),
)
opDadosCuidador = (
    (f"Cuidador", f"Cuidador"),
    (f"Participante", f"Participante"),
    (f"Familiar", f"Familiar"),
     
)
opTestarDoencas = (
        ("Bipolar", "Bipolar"),
        ("Demência", "Demência"),
        ("Depressão Maior", "Depressão Maior"),
        ("Doença Mental", "Doença Mental"),
        ("Epilepsia", "Epilepsia"),
        ("Esquizofrenia", "Esquizofrenia"),
        ("Incapacidade Inteletual", "Incapacidade Inteletual"),
        ("Nada (hiperatividade)", "Nada (hiperatividade)"),
        ("Perturbação Bipolar", "Perturbação Bipolar"),
        ("Não tem", "Outra")
)


class Reference(models.Model):
    nome = models.CharField(max_length=20, default="")

    def __str__(self):
        return f'{self.nome}'


class Administrador(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, blank=True,
                             null=True)
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.user}'


class Doenca(models.Model):
    nome = models.CharField(max_length=50, default="")

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return f'{self.nome}'


class Grupo(models.Model):
    opEscolaridade = (
        ("Analfabeto", "Analfabeto"),
        ("1-4", "1-4"),
        ("5-10", "5-10"),
        ("11+", "11+")
    )

    opPrograma = (
        ("CARE", "CARE"),
        ("COG", "COG"),
    )

    nome = models.CharField(max_length=50)
    #diagnostico = models.ForeignKey(Doenca, on_delete=models.CASCADE, null=True, blank=True)
    localizacao = models.CharField(max_length=20, default="", null=True, blank=True)
    escolaridade = models.CharField(max_length=20, choices=opEscolaridade, default="", blank=True, null=True)
    referenciacao = models.ForeignKey(Reference, on_delete=models.CASCADE, null=True, blank=True)
    nivelGDS = models.IntegerField(default=0)
    programa = models.CharField(max_length=20, choices=opPrograma, default="CARE", blank=True, null=True)

    @property
    def diagnostico(self):
        lista = []
        if self.programa == 'COG':
            for p in self.participantes.all():
                for doenca in p.doencas:
                    lista.append(doenca)
        elif self.programa == 'CARE':
            for c in self.cuidadores.all():
                for doenca in c.doencas:
                    lista.append(doenca)
        return valida_str(most_frequent(lista))
    
    @property
    def localizacao_most_frequent(self):
        lista = []
        if self.programa == 'COG':
            lista = [p.localizacao for p in self.participantes.all()]
        elif self.programa == 'CARE':
            lista = [c.localizacao for c in self.cuidadores.all()]
        return valida_str(most_frequent(lista))

    @property
    def escolaridade_most_frequent(self):
        lista = []
        if self.programa == 'COG':
            lista = [p.escolaridade for p in self.participantes.all()]
        elif self.programa == 'CARE':
            lista = [c.escolaridade for c in self.cuidadores.all()]

        return valida_str(most_frequent(lista))

    @property
    def referenciacao_most_frequent(self):
        lista = []
        if self.programa == 'COG':
            lista = [p.referenciacao.nome for p in self.participantes.all() if p.referenciacao is not None]
        elif self.programa == 'CARE':
            lista = [c.referenciacao.nome for c in self.cuidadores.all() if c.referenciacao is not None]
        return valida_str(most_frequent(lista))

    @property
    def diagnostico_most_frequent(self):
        lista = []
        if self.programa == 'COG':
            for p in self.participantes.all():
                for doenca in p.doencas:
                    lista.append(doenca)
        elif self.programa == 'CARE':
            for c in self.cuidadores.all():
                for doenca in c.doencas:
                    lista.append(doenca)
        return valida_str(most_frequent(lista))

    @property
    def participantes_ou_cuidadores(self):
        lista = []
        for p in self.participantes.all():
            lista.append(p)

        for c in self.cuidadores.all():
            lista.append(c)

        return lista

    @property
    def nr_membros(self):
        return len(self.cuidadores.all()) + len(self.participantes.all()) + len(self.facilitadores.all()) + len(
            self.dinamizadores.all())

    def __str__(self):
        return f'{self.nome}'

    @property
    def sessoes_realizadas(self):
        sessoesRealizadas = 0

        for sessao in self.sessoes.all():
            if sessao.estado == 'R':
                sessoesRealizadas += 1

        return sessoesRealizadas


class Evento(models.Model):
    data = models.DateTimeField(null=True)

    class Meta:
        abstract = True


class Atividade(models.Model):
    numero = models.IntegerField(default=0)
    nome = models.CharField(max_length=1000, null=True, blank=True)
    descricao = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Atividade {self.numero}: {self.nome}'


class Sessao(models.Model):
    PRESENT = 'P'
    ONLINE = 'O'
    MISTO = 'M'
    REGIME = [
        (PRESENT, "Presencial"),
        (ONLINE, "Online"),
        (MISTO, "Misto")
    ]
    PORREALIZAR = 'PR'
    REALIZADO = 'R'
    ESTADO = [
        (PORREALIZAR, "Por realizar"),
        (REALIZADO, "Realizado"),
    ]

    opPrograma = (
        ("CARE", "CARE"),
        ("COG", "COG"),
        ("GAM", "GAM"),
    )

    nome = models.CharField(max_length=100, blank=True)
    numeroSessao = models.IntegerField(null=True, blank=True)
    tema = models.TextField(max_length=1000, null=True, blank=True)
    dinamizadores = models.CharField(max_length=1000, null=True, blank=True)
    componentes = models.CharField(max_length=1000, null=True, blank=True)
    instrumentoAvaliacao = models.TextField(max_length=1000, null=True, blank=True)
    programa = models.CharField(max_length=20, choices=opPrograma, default="CARE", blank=True, null=True)
    materiais = models.FileField(upload_to='materiais/', null=True, blank=True)

    @property
    def objetivos(self):
        objetivos_partes = ""
        for parte in self.partes:
            objetivos_partes += f"* {parte.objetivo}"
        return objetivos_partes

    def __str__(self):
        return f'({self.programa}) Sessão {self.numeroSessao}. {self.nome}'


def img_path(instance, filename):
    return f'img/{filename}'


class Imagem(models.Model):
    nome = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to=img_path, blank=True, null=True)

    def __str__(self):
        return self.nome


class Opcao(models.Model):
    resposta = models.CharField(max_length=300, default="")
    cotacao = models.IntegerField(default=0, blank=True, null=True)
    imagem = models.ForeignKey(Imagem, default=None, null=True, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f'{self.resposta}'


class Pergunta(models.Model):
    INICIAL = 'I'
    DESENVOLVIMENTO = 'D'
    FINAL = 'F'
    FASE = [
        (INICIAL, "Inicial"),
        (DESENVOLVIMENTO, "Desenvolvimento"),
        (FINAL, "Final")
    ]
    fase = models.CharField(max_length=10, choices=FASE, null=True, blank=True, default='I')
    sessao_numero = models.IntegerField(default=0, blank=True, null=True)
    ordem = models.IntegerField(default=0)
    texto = models.CharField(max_length=200)
    opcoes = models.ManyToManyField(Opcao, blank=True, default=None)

    def __str__(self):
        return f'{self.texto}'


class Pergunta_Exercicio(models.Model):
    TIPOS = [
        ("APENAS_MOSTRAR", "Apenas Mostrar"),
        ("UPLOAD_FOTOGRAFIA", "Upload Fotografia"),
        ("RESPOSTA_ESCRITA", "Resposta Escrita"),
        ("ESCOLHA_MULTIPLA", "Escolha Múltipla"),
    ]

    nome = models.CharField(max_length=100, default='', blank=True, null=True)
    postexto = models.CharField(max_length=100, default='', blank=True, null=True)
    tipo_resposta = models.CharField(max_length=50, choices=TIPOS)
    opDificuldade = (
        ("A", "A"),
        ("B", "B"),
        ("Indefinido", "Indefinido")
    )
    dificuldade = models.CharField(max_length=20, choices=opDificuldade, default="Indefinido", blank=False, null=False)
    opcoes = models.ManyToManyField(Opcao, blank=True, default=None)

    def __str__(self):
        if self.dificuldade in ['A', 'B']:
            dif = f'({self.dificuldade})'
        else:
            dif = ''
        return f'{dif} {self.nome}'


class Parte_Exercicio(models.Model):
    nome = models.CharField(max_length=100)
    ordem = models.IntegerField(default=0)
    descricao = models.TextField(max_length=1000, null=True, blank=True)
    imagens = models.ManyToManyField(Imagem, default=None, blank=True)
    duracao = models.IntegerField(default=0)
    perguntas = models.ManyToManyField(Pergunta_Exercicio, blank=True, default=None)

    def __str__(self):
        ex_numeros = []
        for x in self.exercicios.all():
            ex_numeros.append(x.numero)
        return f'Exercício {ex_numeros} - parte {self.ordem} - {self.nome}'


class SessaoDoGrupo(models.Model):
    PRESENT = 'P'
    ONLINE = 'O'
    MISTO = 'M'
    REGIME = [
        (PRESENT, "Presencial"),
        (ONLINE, "Online"),
        (MISTO, "Misto")
    ]
    PORREALIZAR = 'PR'
    EMCURSO = 'EC'
    REALIZADO = 'R'
    ESTADO = [
        (PORREALIZAR, "Por realizar"),
        (EMCURSO, "Em curso"),
        (REALIZADO, "Realizado"),
    ]

    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, blank=True, related_name='sessoes')
    regime = models.CharField(max_length=20, choices=REGIME, null=True, blank=True, default=PRESENT)
    estado = models.CharField(max_length=20, choices=ESTADO, null=True, blank=True, default=PORREALIZAR)
    data = models.DateTimeField(null=True)
    inicio = models.DateTimeField(null=True, blank=True)
    fim = models.DateTimeField(null=True, blank=True)
    concluido = models.BooleanField(default=False)
    sessao = models.ForeignKey(Sessao, on_delete=models.CASCADE, blank=True, null=True, related_name='sessoes')
    parte_ativa = models.ForeignKey(Parte_Exercicio, models.CASCADE, blank=True, null=True, related_name='sessoes')
    relatorio = models.FileField(upload_to='relatorios/', null=True, blank=True)
    diario_bordo = models.FileField(upload_to='diarios/', null=True, blank=True)

    def __str__(self):
        return f'Sessao {self.sessao} do grupo {self.grupo}'

    def parte_atual(self):
        for pg in self.parteGrupos.all():
            if pg.em_progresso:
                return pg


class Questionario(models.Model):
    nome = models.CharField(max_length=50, default="")
    topico = models.CharField(max_length=300, default="", blank=True, null=True)
    perguntas = models.ManyToManyField(Pergunta, blank=True, default=None)
    continuacaoDe = models.ForeignKey(Sessao, blank=True, on_delete=models.CASCADE, null=True, default=None)
    concluido = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.nome}'


class InformacaoSensivel(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=True, null=True)
    telemovel = models.CharField(max_length=20, default="987654321", blank=True, null=True)
    imagem = models.ImageField(null=True, blank=True, upload_to='images/')

    def erase_sensitive_info(self):
        nome = None
        email = None
        telemovel = None
        image = None
        self.save()

    def __str__(self):
        return self.nome


class Utilizador(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, blank=True,
                             null=True)
    

    opSexo = (
        ("Feminino", "Feminino"),
        ("Masculino", "Masculino"),
        ("Outros", "Outros")
    )
    info_sensivel = models.ForeignKey(InformacaoSensivel, on_delete=models.CASCADE, default=None, blank=True, null=True)
    sexo = models.CharField(max_length=20, choices=opSexo, default="", blank=False, null=False)
    nascimento = models.DateField(null=True, blank=True)
    data_entrada = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    nacionalidade = models.CharField(max_length=20, default="", blank=True, null=True)
    localizacao = models.CharField(max_length=20, default="", blank=True, null=True)

    class Meta:
        abstract = True

    @property
    def nome(self):
        return self.info_sensivel.nome

    @property
    def email(self):
        return self.info_sensivel.email

    @property
    def telemovel(self):
        return self.info_sensivel.telemovel

    @property
    def imagem(self):
        return self.info_sensivel.imagem

    @property
    def idade(self):
        today = datetime.now()
        # print(today)
        return today.year - self.nascimento.year - (
                    (today.month, today.day) < (self.nascimento.month, self.nascimento.day))

    @property
    def nascimento_string(self):
        return self.nascimento.strftime('%Y-%m-%d')


class Cuidador(Utilizador):
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

    avaliador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, blank=True,
                                  null=True, related_name='cuidadores')

    escolaridade = models.CharField(max_length=20, choices=opEscolaridade, default="1-4", blank=False, null=False)
    referenciacao = models.ForeignKey(Reference, on_delete=models.CASCADE, blank=True, null=True)
    # referenciacao é um charfield, devia ser um ManyToManyField
    regime = models.CharField(max_length=20, choices=opRegime, default="Online", blank=False, null=False)
    grupo = models.ManyToManyField(Grupo, blank=True, related_name='cuidadores')

    residencia = models.CharField(max_length=20, choices=opResidencia, default="Urbana", blank=True, null=True)
    situacaoLaboral = models.CharField(max_length=20, choices=opSituacaoLaboral, default="Reformado(a)", blank=True,
                                       null=True)
    profissaoPrincipal = models.CharField(max_length=100, default="", blank=True, null=True)
    comorbilidades = models.CharField(max_length=100, default="", blank=True, null=True)
    diagnosticoPrincipal = models.CharField(max_length=100, choices=opTestarDoencas, default="Alzheimer", blank=True, null=True)
    situacaoEconomica = models.CharField(max_length=20, choices=opSituacaoEconomica, default="Satisfatória", blank=True,
                                         null=True)
    estadoCivil = models.CharField(max_length=30, choices=opEstadoCivil, default="Solteiro(a)", blank=True, null=True)
    agregadoFamiliar = models.CharField(max_length=35, choices=opAgregadoFamiliar, default="Vive sozinho(a)",
                                        blank=True, null=True)
    temFilhos = models.BooleanField(default=False, blank=True, null=True)
    nrFilhos = models.IntegerField(default=0, blank=True, null=True)
    autoAvaliacaoEstadoSaude = models.CharField(max_length=30, choices=opEstadoSaude, default="Nem mau nem bom",
                                                blank=True, null=True)
    diagnosticos = models.ManyToManyField(Doenca, related_name='cuidadores', default=None, null=True, blank=True)
    motivoDependecia = models.CharField(max_length=100, choices=opDependencia, default="Demência/Doença Neurocognitiva (cognitiva adquirida)", blank=True, null=True)
    viveComParticipante = models.CharField(max_length=100, choices=(("Sim", "Sim"), ("Não","Não")), default="Sim", blank=True, null=True)
    
    # guarda o nr de prestadores de cuidados
    prestadoresCuidadosFamiliares = models.IntegerField(default=0, blank=True, null=True)
    prestadoresCuidadosAmigos = models.IntegerField(default=0, blank=True, null=True)
    prestadoresCuidadosVizinhos = models.IntegerField(default=0, blank=True, null=True)
    prestadoresCuidadosProfissionaisSAD = models.IntegerField(default=0, blank=True, null=True)
    prestadoresCuidadosProfissionaisCD = models.IntegerField(default=0, blank=True, null=True)
    prestadoresCuidadosOutros = models.IntegerField(default=0, blank=True, null=True)

    # a unidade disto é meses
    tempoCuidados_meses = models.IntegerField(default=0, blank=True, null=True)
    principalMotivoParaCuidar = models.CharField(max_length=1000, default="", blank=True, null=True)
    nivelContribuicao = models.CharField(max_length=100, choices=opNivelContribuicao, default=f"1%-20%", blank=True, null=True)
    periodicidadeCuidado = models.CharField(max_length=100, choices=opPeriodicidade, default="Demência/Doença Neurocognitiva (cognitiva adquirida)", blank=True, null=True)

    diaNormal = models.TextField(default="", blank=True, null=True)

    diaNormal30DiasDormir_minutos = models.IntegerField(default=0, blank=True, null=True)
    diaNormal30DiasTarefasWC_minutos = models.IntegerField(default=0, blank=True, null=True)
    diaNormal30DiasTarefasWC_dias = models.IntegerField(default=0, blank=True, null=True)
    
    diaNormal30DiasTarefasCasa_minutos = models.IntegerField(default=0, blank=True, null=True)
    diaNormal30DiasTarefasCasa_dias = models.IntegerField(default=0, blank=True, null=True)
    
    diaNormal30DiasSupervisao_minutos = models.IntegerField(default=0, blank=True, null=True)
    diaNormal30DiasSupervisao_dias = models.IntegerField(default=0, blank=True, null=True)
    
    @property
    def doencas(self):
        participantes = self.participantes.all()
        diagnosticos = []
        for participante in list(participantes):
            diagnosticos += [obj.nome for obj in participante.diagnosticos.all()]
        diagnosticos = set(diagnosticos)  # remove duplicados
        return diagnosticos

    @property
    def doencas_object(self):
        participantes = self.participantes.all()
        diagnosticos = []
        for participante in list(participantes):
            diagnosticos += [obj for obj in participante.diagnosticos.all()]
        diagnosticos = set(diagnosticos)  # remove duplicados
        return diagnosticos

    @property
    def doencas_string(self):
        d_str = ', '.join(self.doencas)
        if len(d_str) < 2:
            return None
        else:
            return d_str

    @property
    def lista_nomes_participantes(self):
        return [participante.info_sensivel.nome for participante in self.participantes.all()]

    @property
    def lista_nomes_documents(self):
        return [documents.name for documents in self.documents.all()]

    @property
    def lista_description_documents(self):
        return [documents.description for documents in self.documents.all()]

    @property
    def proximoAgendamento(self):
        agendamentos = self.parteDoUtilizador.filter(data__gt=datetime.today()).order_by("data")
        if len(agendamentos) > 0:
            return f"{agendamentos[0].data.strftime('%d/%m/%Y')}"
        else:
            return f"Sem agendamentos"

    @property
    def nrPresencas(self):
        nrPresencas = 0

        for presenca in self.presencas.all():
            if (presenca.mode == 'P') or (presenca.mode == 'O'):
                nrPresencas += 1

        return nrPresencas

    @property
    def get_referenciacao(self):
        return valida_str(self.referenciacao.nome)

    def __str__(self):
        return f'{self.info_sensivel.nome}'


class Mentor(Utilizador):
    grupo = models.ManyToManyField(Grupo, blank=True, related_name='mentores')
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def get_reference(self):
        return valida_str(self.reference.nome)
    
    def __str__(self):
        if self.info_sensivel is not None:
            return f'{self.info_sensivel.nome}'
        return ''
    
class Colaborador(Utilizador):
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def get_reference(self):
        return valida_str(self.reference.nome)
    
    def __str__(self):
        if self.info_sensivel:
            return f'{self.info_sensivel.nome}'
        return ''


class DinamizadorConvidado(Utilizador):
    funcao = models.CharField(max_length=20, default="")
    grupo = models.ManyToManyField(Grupo, blank=True, related_name='dinamizadores')
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def get_reference(self):
        return valida_str(self.reference.nome)
    
    def __str__(self):
        if self.info_sensivel is not None:
            return f'{self.info_sensivel.nome}'
        return ''

class Avaliador(Utilizador):
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def get_reference(self):
        return valida_str(self.reference.nome)
    
    def __str__(self):
        return f'{self.user}'

class Documents(models.Model):
    name = models.CharField(max_length=200, default="")
    description = models.CharField(max_length=200, default="", blank=True, null=True)
    cuidador = models.ManyToManyField(Cuidador, blank=True, related_name='documents')
    file = models.FileField(null=True, blank=True, upload_to='files/')

    def __str__(self):
        return f'{self.name}'

    ####################


# Grupo(Grupo):
#     def __str__(self):
#         return f'{self.nome}'

class Participante(Utilizador):
    
    escolaridade = models.CharField(max_length=20, choices=opEscolaridade, default="1-4", blank=True, null=False)
    residencia = models.CharField(max_length=20, choices=opResidencia, default="Urbana", blank=True, null=True)
    situacaoLaboral = models.CharField(max_length=20, choices=opSituacaoLaboral, default="Reformado(a)", blank=True,
                                       null=True)
    
    dadosCuidador = models.CharField(max_length=20, choices=opDadosCuidador, default="Participante", blank=True, null=True)
    profissaoPrincipal = models.CharField(max_length=100, default="", blank=True, null=True)
    comorbilidades = models.CharField(max_length=100, default="", blank=True, null=True)
    situacaoEconomica = models.CharField(max_length=20, choices=opSituacaoEconomica, default="Satisfatória", blank=True,
                                         null=True)
    # Diagnostico Principal
    diagnosticoPrincipal = models.CharField(max_length = 2000,choices=opTestarDoencas, default="Alzheimer", blank=True, null=True)
    estadoCivil = models.CharField(max_length=30, choices=opEstadoCivil, default="Solteiro(a)", blank=True, null=True)
    agregadoFamiliar = models.CharField(max_length=35, choices=opAgregadoFamiliar, default="Vive sozinho(a)",
                                        blank=True, null=True)
    temFilhos = models.BooleanField(default=False, blank=True, null=True)
    nrFilhos = models.IntegerField(default=0, blank=True, null=True)
    autoAvaliacaoEstadoSaude = models.CharField(max_length=30, choices=opEstadoSaude, default="Nem mau nem bom",
                                                blank=True, null=True)
    diagnosticos = models.ManyToManyField(Doenca, related_name='participantes', default=None, null=True, blank=True)
    referenciacao = models.ForeignKey(Reference, on_delete=models.CASCADE, blank=True, null=True)
    nivel_gds = models.IntegerField(default=1, validators=[
        MaxValueValidator(7),
        MinValueValidator(1)
    ])
    grupo = models.ManyToManyField(Grupo, blank=True, related_name='participantes')
    cuidadores = models.ManyToManyField(Cuidador, blank=True, related_name='participantes')
    avaliador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, blank=True,
                                  null=True, related_name='participantes')

    @property
    def doencas(self):
        diagnosticos = []
        diagnosticos += [obj.nome for obj in self.diagnosticos.all()]
        diagnosticos = set(diagnosticos)  # remove duplicados
        return diagnosticos

    @property
    def proximoAgendamento(self):
        agendamentos = self.parteDoUtilizador.filter(data__gt=datetime.today()).order_by("data")
        if len(agendamentos) > 0:
            return f"{agendamentos[0].data.strftime('%d/%m/%Y')}"
        else:
            return f"Sem agendamentos"

    def doencas_string(self):
        d_str = ', '.join(self.doencas)
        if len(d_str) < 2:
            return None
        else:
            return d_str
    
    @property
    def get_referenciacao(self):
        return valida_str(self.referenciacao.nome)

    def __str__(self):
        return f'{self.info_sensivel.nome}'


class Facilitador(Utilizador):
    grupo = models.ManyToManyField(Grupo, blank=True, related_name='facilitadores')

    def __str__(self):
        return f'{self.nome}'

class Exercicio(models.Model):
    sessao = models.ManyToManyField(Sessao, default=None, blank=True, related_name='exercicios')
    dominio = models.CharField(max_length=100, default='')
    numero = models.IntegerField(default=0)
    duracao = models.IntegerField(default=0)
    descricao = models.TextField(max_length=1000, null=True, blank=True)
    material = models.TextField(max_length=1000, null=True, blank=True)
    instrucao = models.TextField(max_length=2000, null=True, blank=True)
    instrucao_participante = models.TextField(max_length=2000, null=True, blank=True)
    partes_do_exercicio = models.ManyToManyField(Parte_Exercicio, blank=True, related_name='exercicios')

    def __str__(self):
        return f'Exercício {self.numero}'


class Parte(models.Model):
    INICIAL = 'I'
    DESENVOLVIMENTO = 'D'
    FINAL = 'F'
    FASE = [
        (INICIAL, "Inicial"),
        (DESENVOLVIMENTO, "Desenvolvimento"),
        (FINAL, "Final")
    ]
    fase = models.CharField(max_length=10, choices=FASE, null=True, blank=True)
    objetivo = models.TextField(max_length=1000, null=True, blank=True)
    descricao = models.TextField(max_length=1000, null=True, blank=True)
    materiais = models.TextField(max_length=1000, null=True, blank=True)
    duracao = models.IntegerField(null=True, blank=True)
    atividades = models.ManyToManyField(Atividade, blank=True)
    apresentacao = models.FileField(upload_to='apresentacoes/', null=True, blank=True)
    apresentacao_esquizofrenia = models.FileField(upload_to='apresentacao_esquizofrenia/', null=True, blank=True)
    apresentacao_perturbacao_bipolar = models.FileField(upload_to='apresentacao_perturbacao_bipolar/', null=True, blank=True)
    apresentacao_demencia = models.FileField(upload_to='apresentacao_demencia/', null=True, blank=True)
    apresentacao_incapacidade_intelectual = models.FileField(upload_to='apresentacao_incapacidade_intelectual/', null=True, blank=True)
    # observacoes = models.TextField(max_length=1000, null=True, blank=True)
    sessao = models.ForeignKey(Sessao, blank=True, related_name='partes', on_delete=models.CASCADE, null=True,
                               default=None)
    questionarios = models.ManyToManyField(Questionario, blank=True)
    ordem = models.IntegerField(default=0)

    # para apagar mas rever como fazer ao certo
    # tempo = models.IntegerField(null=True, blank=True, default=0)
    # concluida = models.BooleanField(default=False)
    @property
    def numeroSessao(self):
        return self.sessao.numeroSessao

    def __str__(self):
        return f'Sessao n°:{self.numeroSessao}, {self.fase}, objetivo: {self.objetivo}'



class ParteGrupo(models.Model):
    sessaoGrupo = models.ForeignKey(SessaoDoGrupo, on_delete=models.CASCADE, blank=True, related_name='parteGrupos')
    parte = models.ForeignKey(Parte, on_delete=models.CASCADE, default=None, blank=True, null=True,
                              related_name='partesGrupos')
    exercicio = models.ForeignKey(Exercicio, on_delete=models.CASCADE, default=None, blank=True, null=True,
                                  related_name='partesGrupos')

    inicio = models.DateTimeField(null=True, blank=True)
    fim = models.DateTimeField(null=True, blank=True)
    concluido = models.BooleanField(default=False)

    @property
    def em_progresso(self):
        return not self.concluido

    @property
    def duracao(self):
        if self.fim != None and self.inicio != None:
            return (self.fim - self.inicio).seconds
        elif self.fim == None and self.inicio != None:
            return (datetime.utcnow() - self.inicio).seconds
        else:
            return 0

    @property
    def duracao_minutos(self):
        return self.duracao // 60

    @property
    def duracao_em_horas_minutos(self):

        if self.fim != None and self.inicio != None:
            seconds = (self.fim - self.inicio).seconds
        elif self.fim == None and self.inicio != None:
            seconds = (datetime.utcnow() - self.inicio).seconds
        else:
            seconds = 0

        h = math.floor(seconds / 3600)
        m = math.floor(seconds % 3600 / 60)
        s = math.floor(seconds % 3600 % 60)

        hDisplay = ""
        if h > 0:
            hDisplay = str(h)
        mDisplay = "0"
        if m > 0:
            mDisplay = str(m)

        return hDisplay + mDisplay

    def __str__(self):
        if self.parte:
            return f'Parte {self.parte} da {self.sessaoGrupo}'
        else:
            return f'Exercício {self.exercicio} da {self.sessaoGrupo}'


def submission_path(instance, filename):
    return f'users/{instance.participante.id}/{instance.id}-{filename}'


class Resposta(models.Model):
    parte_grupo = models.ForeignKey(ParteGrupo, on_delete=models.CASCADE, null=True, blank=True, default=None)
    sessao_grupo = models.ForeignKey(SessaoDoGrupo, on_delete=models.CASCADE, null=True, blank=True, default=None)
    parte_exercicio = models.ForeignKey(Parte_Exercicio, on_delete=models.CASCADE, null=True, blank=True, default=None)
    participante = models.ForeignKey(Participante, default=None, blank=True, null=True, on_delete=models.CASCADE)
    pergunta = models.ForeignKey(Pergunta_Exercicio, default=None, blank=True, null=True, on_delete=models.CASCADE)
    resposta_escrita = models.TextField(max_length=2000, default=None, blank=True, null=True)
    resposta_submetida = models.ImageField(upload_to=submission_path, blank=True, null=True)
    resposta_escolha = models.ForeignKey(Opcao, on_delete=models.CASCADE, null=True, blank=True, default=None,
                                         related_name="resp")

    # NN Apontamento fica aqui ou noutra tabela só de apontamentos?
    apontamento = models.TextField(max_length=2000, default=None, blank=True, null=True)
    data = models.DateTimeField(auto_now_add=True, null=True)

    certo = models.BooleanField(default=None, blank=True, null=True)

    def __str__(self):
        if self.participante is not None:
            return f'{self.parte_grupo}' + ' - ' +   f'{self.participante.nome}' + ' - ' f'{self.pergunta}'
        return 'Sem Participante'

class Escolha(models.Model):
    opcao = models.ForeignKey(Opcao, on_delete=models.CASCADE, null=True, blank=True, default=None)
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE, null=True, default=None, related_name="escolhas")
    resposta_escrita = models.CharField(max_length=750, default=None, null=True, blank=True)
    utilizador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, blank=True,
                                   null=True)
    parte_grupo = models.ForeignKey(ParteGrupo, on_delete=models.CASCADE, null=True, blank=True, default=18)
    sessao_grupo = models.ForeignKey(SessaoDoGrupo, on_delete=models.CASCADE, null=True, default=None)


class Partilha(models.Model):
    partilha_dinamizador = models.ForeignKey(DinamizadorConvidado, on_delete=models.CASCADE, default="", null=True,
                                             blank=True,
                                             related_name='partilha_dinamizador')
    partilha_mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, default="", null=True,
                                        blank=True,
                                        related_name='partilha_mentor')
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE, blank=True, null=True)
    sessao_grupo = models.ForeignKey(SessaoDoGrupo, on_delete=models.CASCADE, null=True, default=None)
    cuidador = models.ForeignKey(Cuidador, on_delete=models.CASCADE, blank=True, null=True)
    partilha = models.TextField()
    data = models.DateTimeField(auto_now_add=True, null=True)
    imagem = models.FileField(upload_to="images/", null=True, blank=True)
    ficheiro = models.FileField(upload_to="ficheiros_partilhas/", null=True, blank=True)
    aprovada = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.partilha}'

    def data_str(self):
        formato_saida = "%d/%m/%Y %H:%M"
        data_saida = self.data.strftime(formato_saida)
        return data_saida

    def hora_str(self):
        formato_saida = "%H:%M"
        data_saida = self.data.strftime(formato_saida)
        return data_saida

class PartilhaGrupo(models.Model):
    partilha_dinamizador = models.ForeignKey(DinamizadorConvidado, on_delete=models.CASCADE, default="", null=True,
                                             blank=True,
                                             related_name='partilha_grupo_dinamizador')
    partilha_mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, default="", null=True,
                                        blank=True,
                                        related_name='partilha_grupo_mentor')
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    descricao = models.TextField()
    data = models.DateTimeField(auto_now_add=True, null=True)
    sessao_grupo = models.ForeignKey(SessaoDoGrupo, on_delete=models.CASCADE, null=True, default=None)
    imagem = models.FileField(upload_to="images/", null=True, blank=True)
    ficheiro = models.FileField(upload_to="ficheiros_partilhas/", null=True, blank=True)

    def __str__(self):
        return f'{self.descricao}'

    def data_str(self):
        formato_saida = "%d/%m/%Y %H:%M"
        data_saida = self.data.strftime(formato_saida)
        return data_saida

    def hora_str(self):
        formato_saida = "%H:%M"
        data_saida = self.data.strftime(formato_saida)
        return data_saida

###################################  COG ########################


# class Auxiliar(Utilizador):
#     grupo = models.ManyToManyField(Grupo, blank=True, related_name='auxiliares')

#     def __str__(self):
#         return f'{self.nome}'


###################################  Avalia ########################

# class Avaliador(Utilizador):
#     def __str__(self):
#         return f'{self.nome}'


class Nota(models.Model):
    opTipo = (
        ("Atividades", "Atividades"),
        ("Gerais", "Gerais"),
        ("Sessão", "Sessão"),
    )
    sessao_grupo = models.ForeignKey(SessaoDoGrupo, on_delete=models.CASCADE, null=True, default=None)
    anotador_dinamizador = models.ForeignKey(DinamizadorConvidado, on_delete=models.CASCADE, default="", null=True,
                                             blank=True,
                                             related_name='notas_dinamizador_sobre_cuidador')
    anotador_mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, default="", null=True,
                                        blank=True,
                                        related_name='notas_menor_sobre_participante')
    cuidador = models.ForeignKey(Cuidador, on_delete=models.CASCADE, default="", null=True, blank=True,
                                 related_name='notas')
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE, null=True, blank=True)
    tipo = models.CharField(max_length=20, choices=opTipo, default="Gerais", blank=True, null=True)
    tituloNota = models.CharField(max_length=20, default="", null=True, blank=True)
    nota = models.TextField()
    data = models.DateTimeField(auto_now_add=True, null=True)

    # podemos ter alternativamente dois campos: criado, modificado sendo o segundo atualizado se modificada a nota
    # https://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-add

    def __str__(self):
        return f'{self.nota}'

    def data_str(self):
        formato_saida = "%d/%m/%Y %H:%M"
        data_saida = self.data.strftime(formato_saida)
        return data_saida

    def hora_str(self):
        formato_saida = "%H:%M"
        data_saida = self.data.strftime(formato_saida)
        return data_saida


# class GrupoAvalia(Grupo):
#     avaliador = models.ForeignKey(Avaliador, on_delete=models.CASCADE)
#     participante = models.ForeignKey(Participante, on_delete=models.CASCADE)

#     def __str__(self):
#         return f'{self.nome}'


class Presenca(Evento):
    # Possibilidade de registar o motivo de noa ter ido a sessao
    PRESENT = 'P'
    ONLINE = 'O'
    PROTOCOLO = 'PR'
    COG = 'CG'
    CARE = 'CR'
    MODES = [
        (PRESENT, "Presencial"),
        (ONLINE, "Online")
    ]
    SESSAO = [
        (PROTOCOLO, "Protocolo"),
        (COG, "Cog"),
        (CARE, "Care")
    ]
    cuidador = models.ForeignKey(Cuidador, on_delete=models.CASCADE, null=True, blank=True,
                                 related_name='presencas')
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='presencas')
    tipoSessao = models.CharField(choices=SESSAO, null=True, blank=True, default=CARE, max_length=20)
    sessaoDoGrupo = models.ForeignKey(SessaoDoGrupo, on_delete=models.CASCADE, null=True, blank=True,
                                      related_name='sessao_grupo')
    # info a recolher no formulário, com checkboxes
    present = models.BooleanField(default=False)
    faltou = models.BooleanField(default=False)
    mode = models.CharField(max_length=20, choices=MODES, null=True, blank=True, default=PRESENT)
    withApp = models.BooleanField(null=True, blank=True)
    descricao = models.TextField(null=True, blank=True)

    def set_faltou(self):
        self.faltou = True
        self.present = False
        self.mode = None
        self.save()

    def set_online(self):
        self.faltou = False
        self.present = True
        self.mode = Presenca.ONLINE
        self.save()

    def set_presencial(self):
        self.faltou = False
        self.present = True
        self.mode = Presenca.PRESENT
        self.save()

    def __str__(self):
        presenca = ""
        if self.present:
            presenca = "presente"
        else:
            presenca = "faltou"
        return f"{self.participante if self.participante is not None else self.cuidador} {presenca} - Modo: {self.mode if self.mode is not None else 'Faltou'}"


class NotaGrupo(models.Model):
    anotador_dinamizador = models.ForeignKey(DinamizadorConvidado, on_delete=models.CASCADE, default="", null=True,
                                             blank=True,
                                             related_name='notas_grupo_dinamizador')
    anotador_mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, default="", null=True,
                                        blank=True,
                                        related_name='notas_grupo_mentor')
    sessao_grupo = models.ForeignKey(SessaoDoGrupo, on_delete=models.CASCADE, null=True)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, null=True)
    notaGrupo = models.TextField()
    data = models.DateTimeField(auto_now_add=True, null=True)

    # podemos ter alternativamente dois campos: criado, modificado sendo o segundo atualizado se modificada a nota
    # https://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-add

    def __str__(self):
        return f'{self.notaGrupo}'

    def data_str(self):
        formato_saida = "%d/%m/%Y %H:%M"
        data_saida = self.data.strftime(formato_saida)
        return data_saida

    def hora_str(self):
        formato_saida = "%H:%M"
        data_saida = self.data.strftime(formato_saida)
        return data_saida

class AvaliacaoParticipante(models.Model):
    validators = [
        MaxValueValidator(5),
        MinValueValidator(1)
    ]
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE, blank=True)
    sessao_grupo = models.ForeignKey(SessaoDoGrupo, on_delete=models.CASCADE, blank=True)
    interesse = models.IntegerField(default=1, validators=validators, blank=True, null=True)
    comunicacao = models.IntegerField(default=1, validators=validators, blank=True, null=True)
    iniciativa = models.IntegerField(default=1, validators=validators, blank=True, null=True)
    satisfacao = models.IntegerField(default=1, validators=validators, blank=True, null=True)
    humor = models.IntegerField(default=1, validators=validators, blank=True, null=True)
    eficacia_relacional = models.IntegerField(default=1, validators=validators, blank=True, null=True)

    submetido_por = models.ForeignKey(Facilitador, on_delete=models.CASCADE, blank=True, null=True, default=None)

    # talvez fazer outra tabela para isto
    observacao = models.TextField(max_length=550, default="", blank=True, null=True)

    def __str__(self):
        return f"Avaliação de {self.participante.nome} na sessao {self.sessao_grupo.sessao.numeroSessao}"


class AvaliacaoSessao(models.Model):
    validators = [
        MaxValueValidator(5),
        MinValueValidator(1)
    ]
    CHOICES = (
        ("SIM", "Sim"),
        ("NAO", "Não"),
    )

    sessao_grupo = models.ForeignKey(SessaoDoGrupo, on_delete=models.CASCADE, blank=True)
    planificacao_conteudos = models.IntegerField(default=1, validators=validators, blank=True, null=True)
    adq_conteudos = models.IntegerField(default=1, validators=validators, blank=True, null=True)
    adq_materiais = models.IntegerField(default=1, validators=validators, blank=True, null=True)
    adq_tempo = models.IntegerField(default=1, validators=validators, blank=True, null=True)
    grau_dominio = models.IntegerField(default=1, validators=validators, blank=True, null=True)
    necessidade_treino = models.CharField(max_length=10, default="NAO", choices=CHOICES, blank=True, null=True)
    apreciacao_global = models.IntegerField(default=1, validators=validators, blank=True, null=True)
    tipo_treino_competencias = models.TextField(max_length=550, default="", blank=True, null=True)
    # talvez fazer outra tabela para isto

    submetido_por = models.ForeignKey(Facilitador, on_delete=models.CASCADE, blank=True, null=True, default=None)

    observacao = models.TextField(max_length=550, default="", blank=True, null=True)

