from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class Listas(models.Model):
    id = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.nome

    @staticmethod
    def create(nome, id_usuario):
        usuario = get_object_or_404(User, id=id_usuario)
        lista = Listas(nome=nome, id_usuario=usuario)
        lista.save()
        return lista


class Itens(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    id_lista = models.ForeignKey(Listas, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.nome

    @staticmethod
    def create(nome, id_lista):
        lista = get_object_or_404(Listas, id=id_lista)
        item = Itens(nome=nome, id_lista=lista)
        item.save()
        return item
