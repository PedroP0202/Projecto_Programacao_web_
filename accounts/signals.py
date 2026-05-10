from django.apps import apps
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .utils import GROUP_NAME


PORTFOLIO_MODELS = [
    'competencia',
    'docente',
    'formacao',
    'interesse',
    'licenciatura',
    'makingof',
    'projeto',
    'tecnologia',
    'tfc',
    'unidadecurricular',
]


@receiver(post_migrate)
def ensure_portfolio_manager_group(sender, **kwargs):
    if not apps.is_installed('portfolio'):
        return

    group, _ = Group.objects.get_or_create(name=GROUP_NAME)
    codenames = [
        f'{action}_{model_name}'
        for model_name in PORTFOLIO_MODELS
        for action in ['add', 'change', 'delete', 'view']
    ]
    permissions = Permission.objects.filter(
        content_type__app_label='portfolio',
        content_type__model__in=PORTFOLIO_MODELS,
        codename__in=codenames,
    )
    group.permissions.set(permissions)
