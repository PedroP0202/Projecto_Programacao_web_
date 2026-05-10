import uuid
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone


class MagicLoginToken(models.Model):
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='magic_login_tokens',
    )
    redirect_path = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Link mágico para {self.user}'

    @property
    def expires_at(self):
        return self.created_at + timedelta(minutes=15)

    def is_valid(self):
        return self.used_at is None and timezone.now() <= self.expires_at

    def mark_as_used(self):
        self.used_at = timezone.now()
        self.save(update_fields=['used_at'])
