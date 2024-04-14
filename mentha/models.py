from django.db import models


PARCEIROS_CHOICES = [
    ('ADEB', 'ADEB'),
    ('ASMAL', 'ASMAL'),
    ('Elo Social', 'Elo Social'),
    ('CVP', 'CVP'),
    ('FamiliarMente', 'FamiliarMente'),
    ('GIRA', 'GIRA'),
]

# Create your models here.
class Contacto(models.Model):

    nome = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    telefone = models.IntegerField(null=True, blank=True)
    referenciacao = models.CharField(max_length=30, blank=True, choices=PARCEIROS_CHOICES)
    distrito = models.CharField(max_length=30, blank=True)
    assunto = models.CharField(max_length=50, blank=False, null=False)
    mensagem = models.TextField(null=False, blank=False)
    data = models.DateTimeField(editable=False, null=True, auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.nome}: {self.assunto}'


class Noticia(models.Model):


    titulo = models.CharField(max_length=125, null=False, blank=False)
    texto = models.TextField(null=False, blank=False)
    data = models.DateField(null=True)
    url = models.URLField(null=True, blank=True)
    imagem = models.ImageField(upload_to = 'mentha/noticias/', null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.titulo}'