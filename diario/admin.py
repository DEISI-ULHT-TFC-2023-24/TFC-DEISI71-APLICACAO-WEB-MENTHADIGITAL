from django.apps import apps
from django.contrib import admin
from import_export.admin import ExportActionMixin
from import_export import resources
from .models import Participante
from import_export import fields, widgets
from .models import InformacaoSensivel

# Register your models here.

app = apps.get_app_config('diario')

for model_name, model in app.models.items():
    admin.site.register(model)


class SensitiveInfoResource(resources.ModelResource):
    class Meta:
        model = InformacaoSensivel  # Replace with your actual sensitive info model

    def __str__(self, obj):
        # Provide a meaningful representation for the sensitive info model
        return f"Sensitive Info: {obj.some_field}"

class ParticipanteResource(resources.ModelResource):
    info_sensivel = fields.Field(column_name='info_sensivel', attribute='info_sensivel', widget=widgets.ForeignKeyWidget(InformacaoSensivel, 'info_sensivel'))
    referenciacao = fields.Field(column_name='referenciacao', attribute='referenciacao', widget=widgets.ForeignKeyWidget(InformacaoSensivel, 'referenciacao'))

    class Meta:
        model = Participante
        fields = ('user', 'opSexo', 'info_sensivel', 'sexo', 'nascimento', 'data_entrada', 'nacionalidade', 'localizacao'
    ,'escolaridade', 'residencia', 'situacaoLaboral', 'profissaoPrincipal', 'situacaoEconomica', 'estadoCivil', 'agregadoFamiliar'
    ,'temFilhos', 'nrFilhos', 'autoAvaliacaoEstadoSaude', 'nivel_gds', 'avaliador')

    def dehydrate_info_sensivel(self, participante):
        return str(participante.info_sensivel)

    def dehydrate_referenciacao(self, participante):
        return str(participante.referenciacao)


if admin.site.is_registered(Participante):
    admin.site.unregister(Participante)

class ParticipanteAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = ParticipanteResource
    list_display = ('user', 'opSexo', 'info_sensivel', 'sexo', 'nascimento', 'data_entrada', 'nacionalidade', 'localizacao'
    ,'escolaridade', 'residencia', 'situacaoLaboral', 'profissaoPrincipal', 'situacaoEconomica', 'estadoCivil', 'agregadoFamiliar'
    ,'temFilhos', 'nrFilhos', 'autoAvaliacaoEstadoSaude', 'referenciacao', 'nivel_gds', 'avaliador')

admin.site.register(Participante, ParticipanteAdmin)