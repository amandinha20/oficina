from django.db import models

# Create your models here.

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    telefone = models.CharField(max_length=15, blank=True)
    endereco = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nome} ({self.cpf})"
