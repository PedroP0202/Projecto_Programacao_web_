from django.conf import settings
from django.db import models
from django.urls import reverse


class Artigo(models.Model):
    titulo = models.CharField(max_length=160)
    texto = models.TextField()
    fotografia = models.ImageField(upload_to='artigos/', null=True, blank=True)
    link_externo = models.URLField('link externo', null=True, blank=True)
    data_criacao = models.DateTimeField('data de criação', auto_now_add=True)
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='artigos',
    )

    class Meta:
        ordering = ['-data_criacao']
        verbose_name = 'artigo'
        verbose_name_plural = 'artigos'

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('artigos:lista')

    @property
    def total_likes(self):
        return self.likes.count()


class Like(models.Model):
    artigo = models.ForeignKey(Artigo, on_delete=models.CASCADE, related_name='likes')
    utilizador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes_artigos',
        null=True,
        blank=True,
    )
    session_key = models.CharField(max_length=40, null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['artigo', 'utilizador'],
                condition=models.Q(utilizador__isnull=False),
                name='unique_like_artigo_utilizador',
            ),
            models.UniqueConstraint(
                fields=['artigo', 'session_key'],
                condition=models.Q(session_key__isnull=False),
                name='unique_like_artigo_session',
            ),
        ]

    def __str__(self):
        dono = self.utilizador or self.session_key
        return f'Like em {self.artigo} por {dono}'


class Comentario(models.Model):
    artigo = models.ForeignKey(Artigo, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comentarios_artigos',
        null=True,
        blank=True,
    )
    nome_autor = models.CharField(max_length=100, null=True, blank=True, help_text="Para utilizadores não autenticados")
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['data_criacao']
        verbose_name = 'comentário'
        verbose_name_plural = 'comentários'

    def __str__(self):
        nome = self.autor.username if self.autor else self.nome_autor or "Anónimo"
        return f'Comentário de {nome} em {self.artigo}'


class Rating(models.Model):
    artigo = models.ForeignKey(Artigo, on_delete=models.CASCADE, related_name='ratings')
    valor = models.IntegerField()
    utilizador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ratings_artigos',
        null=True,
        blank=True,
    )
    session_key = models.CharField(max_length=40, null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['artigo', 'utilizador'],
                condition=models.Q(utilizador__isnull=False),
                name='unique_rating_artigo_utilizador',
            ),
            models.UniqueConstraint(
                fields=['artigo', 'session_key'],
                condition=models.Q(session_key__isnull=False),
                name='unique_rating_artigo_session',
            ),
        ]

    def __str__(self):
        dono = self.utilizador or self.session_key
        return f'Rating de {self.valor} em {self.artigo} por {dono}'
