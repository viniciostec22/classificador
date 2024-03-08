import os
from django.db import models
from django.contrib.auth.models import User

class Imagem(models.Model):
    image = models.ImageField(upload_to='galeria')
    data_criacao = models.DateTimeField(auto_now_add=True)
    classe = models.BooleanField(blank=False, null=False, default=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

class Doenca(models.Model):
    nome = models.CharField(max_length=100)
    # descricao = models.TextField()

    def __str__(self):
        return self.nome

class Analise(models.Model):
    imagem = models.ForeignKey(Imagem, on_delete=models.CASCADE)
    doenca = models.ForeignKey(Doenca, on_delete=models.CASCADE)
    especialista = models.ForeignKey(User, on_delete=models.CASCADE)
    data_analise = models.DateTimeField(auto_now_add=True)
  
    
