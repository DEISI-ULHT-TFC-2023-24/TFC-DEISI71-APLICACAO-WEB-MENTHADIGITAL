# Generated by Django 4.0.1 on 2022-12-16 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentha', '0010_alter_noticia_titulo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticia',
            name='titulo',
            field=models.CharField(max_length=125),
        ),
    ]
