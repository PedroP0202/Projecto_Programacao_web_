from django.db import models


class GrupoMuscular(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class PlanoTreino(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome


class Exercicio(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    grupo_muscular = models.ForeignKey(
        GrupoMuscular,
        on_delete=models.CASCADE,
        related_name='exercicios',
    )
    plano_treino = models.ManyToManyField(
        PlanoTreino,
        related_name='exercicios',
        blank=True,
    )

    def __str__(self):
        return self.nome
