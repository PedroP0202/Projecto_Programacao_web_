import os

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from accounts.signals import ensure_portfolio_manager_group
from accounts.utils import GROUP_NAME


class Command(BaseCommand):
    help = 'Cria ou atualiza um utilizador staff no grupo gestor-portfolio.'

    def handle(self, *args, **options):
        ensure_portfolio_manager_group(sender=None)

        username = os.getenv('DJANGO_MANAGER_USERNAME', 'gestor')
        password = os.getenv('DJANGO_MANAGER_PASSWORD', 'gestor1234')
        email = os.getenv('DJANGO_MANAGER_EMAIL', 'gestor@example.com')

        if 'DJANGO_MANAGER_USERNAME' not in os.environ or 'DJANGO_MANAGER_PASSWORD' not in os.environ:
            self.stdout.write(
                self.style.WARNING(
                    'Variáveis do gestor não definidas; a usar credenciais por omissão.'
                )
            )

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'is_staff': True,
            },
        )

        user.email = email
        user.is_staff = True
        user.set_password(password)
        user.save()

        group = Group.objects.get(name=GROUP_NAME)
        user.groups.add(group)

        action = 'criado' if created else 'atualizado'
        self.stdout.write(
            self.style.SUCCESS(
                f'Utilizador gestor {username} {action} e associado ao grupo {GROUP_NAME}.'
            )
        )
