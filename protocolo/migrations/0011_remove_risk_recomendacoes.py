# Generated by Django 4.2.6 on 2023-12-26 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('protocolo', '0010_rename_recomendacoes_adicionais_risk_recomendacoes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='risk',
            name='recomendacoes',
        ),
    ]