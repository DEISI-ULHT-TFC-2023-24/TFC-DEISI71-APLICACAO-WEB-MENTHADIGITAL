import os
from django import template
from datetime import datetime
from diario.models import *

register = template.Library()


@register.simple_tag
def verifica_se_tem_valores(val, texto):
    temp = str(val)
    if len(temp) >= 1 and val is not None:
        return temp
    else:
        return texto


@register.filter
def filename(value):
    return os.path.basename(value.file.name)


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter
def is_dinamizador(user):
    return DinamizadorConvidado.objects.filter(user=user).exists()


@register.filter
def is_mentor(user):
    return Mentor.objects.filter(user=user).exists()


@register.filter
def is_avaliador(user):
    return Avaliador.objects.filter(user=user).exists()
