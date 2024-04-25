from django.db import models


class Listas(models.Model):
    id = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


class Itens(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    id_lista = models.ForeignKey(Listas, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome
