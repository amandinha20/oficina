from django.db import models
from clientes.models import Cliente

class Veiculo(models.Model):
    placa = models.CharField(max_length=8, unique=True)
    modelo = models.CharField(max_length=50)
    ano = models.IntegerField()
    cor = models.CharField(max_length=30, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.placa} - {self.modelo}"
