from django.contrib import admin
from django.apps import apps
from import_export.admin import ExportActionMixin
from import_export import resources
from import_export import fields, widgets
from .models import Risk
from diario.models import Participante

app = apps.get_app_config('protocolo')

for model_name, model in app.models.items():
    admin.site.register(model)


if admin.site.is_registered(Risk):
    admin.site.unregister(Risk)

class RiskResource(resources.ModelResource):
    parteDoUtilizador = fields.Field(column_name='parteDoUtilizador', attribute='parteDoUtilizador', widget=widgets.ForeignKeyWidget(Risk, 'parteDoUtilizador'))
    class Meta:
        model = Risk  # Replace with your actual sensitive info model
        fields = ('parteDoUtilizador','pat_id', 'data_atual', 'idade', 'sexo', 'peso', 'altura', 'imc',
                  'pressao_arterial', 'colestrol_total', 'colestrol_hdl', 'colestrol_nao_hdl',
                  'hemoglobina_gliciada', 'horas_jejum', 'doenca_cognitiva', 'fumador', 'diabetes',
                  'anos_diabetes', 'avc', 'enfarte', 'doenca_rins', 'doenca_pernas', 'hipercolestrol',
                  'comentario', 'recomendacoes2', 'tg', 'ldl', 'cholhdl', 'batimentos', 'risco_de_enfarte',
                  'relatorio', 'relatorio_word', 'concluido', 'ifcc', 'ngsp', 'eag')

    def dehydrate_parteDoUtilizador(self, risk):
        return str(risk.parteDoUtilizador)

class RiskAdmin(ExportActionMixin, admin.ModelAdmin):

    resource_class = RiskResource

    #check all the fields that you want to display to not have sting out of index or null values filter the fields
    if str == 'parteDoUtilizador':
        list_display = ('pat_id', 'data_atual', 'idade', 'sexo', 'peso', 'altura', 'imc',
                    'pressao_arterial', 'colestrol_total', 'colestrol_hdl', 'colestrol_nao_hdl',
                    'hemoglobina_gliciada', 'horas_jejum', 'doenca_cognitiva', 'fumador', 'diabetes',
                    'anos_diabetes', 'avc', 'enfarte', 'doenca_rins', 'doenca_pernas', 'hipercolestrol',
                    'comentario', 'comentario2', 'tg', 'ldl', 'cholhdl', 'batimentos', 'risco_de_enfarte',
                    'relatorio', 'relatorio_word', 'concluido', 'ifcc_hba1', 'ngsp_hba1', 'eag_hba1')

admin.site.register(Risk, RiskAdmin)