# Generated by Django 4.2.6 on 2023-12-26 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protocolo', '0006_alter_risk_doenca_cognitiva'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='risk',
            name='recomendacoesAdicionais',
        ),
        migrations.AddField(
            model_name='risk',
            name='recomendacoes_adicionais',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
