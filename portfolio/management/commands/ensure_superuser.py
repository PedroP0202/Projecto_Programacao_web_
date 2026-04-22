import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Cria ou atualiza o superuser com base nas variáveis de ambiente.'

    def handle(self, *args, **options):
        username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin1234')
        email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')

        if 'DJANGO_SUPERUSER_USERNAME' not in os.environ or 'DJANGO_SUPERUSER_PASSWORD' not in os.environ:
            self.stdout.write(
                self.style.WARNING(
                    'Variáveis do superuser não definidas; a usar credenciais por omissão.'
                )
            )

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'is_staff': True,
                'is_superuser': True,
            },
        )

        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        action = 'criado' if created else 'atualizado'
        self.stdout.write(self.style.SUCCESS(f'Superuser {username} {action} com sucesso.'))
