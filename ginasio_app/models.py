from django.db import models
from django.utils import timezone
import secrets


def generate_api_key():
    """Gera uma chave segura e aleatória."""
    return secrets.token_urlsafe(32)


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


# ──────────────────────────────────────────────
# Modelo para guardar e gerir chaves de acesso à API
# ──────────────────────────────────────────────

class APIKey(models.Model):
    name = models.CharField(max_length=100, help_text="Nome de quem vai usar a chave")
    key = models.CharField(max_length=255, unique=True, default=generate_api_key)
    is_active = models.BooleanField(default=True)
    expiration_date = models.DateTimeField(help_text="Data e hora de expiração da chave")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "API Key"
        verbose_name_plural = "API Keys"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {'Ativa' if self.is_active else 'Inativa'}"

    def is_valid(self):
        """Verifica se a chave está ativa e se ainda não expirou."""
        return self.is_active and self.expiration_date > timezone.now()
