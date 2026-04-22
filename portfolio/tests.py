import os
from io import StringIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .models import Licenciatura, TFC

class HomeViewTests(TestCase):
    def test_home_page_loads_without_data(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Portfólio Académico')

    def test_home_page_shows_course_name(self):
        Licenciatura.objects.create(
            nome='Engenharia Informática',
            apresentacao='Curso simples e funcional.',
            objetivos='Aprender a programar.',
            competencias='Python, Django e bases de dados.',
            saidas_profissionais='Desenvolvimento de software.',
        )

        response = self.client.get(reverse('home'))

        self.assertContains(response, 'Engenharia Informática')


class DeployCommandTests(TestCase):
    def test_ensure_superuser_uses_defaults_when_environment_is_missing(self):
        with patch.dict(os.environ, {}, clear=True):
            call_command('ensure_superuser')

        user = get_user_model().objects.get(username='admin')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password('admin1234'))

    def test_ensure_superuser_creates_admin_from_environment(self):
        with patch.dict(
            os.environ,
            {
                'DJANGO_SUPERUSER_USERNAME': 'admin',
                'DJANGO_SUPERUSER_PASSWORD': 'admin1234',
                'DJANGO_SUPERUSER_EMAIL': 'admin@example.com',
            },
            clear=False,
        ):
            call_command('ensure_superuser')

        user = get_user_model().objects.get(username='admin')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password('admin1234'))

    def test_seed_portfolio_creates_core_data(self):
        stdout = StringIO()

        call_command('seed_portfolio', stdout=stdout)

        licenciatura = Licenciatura.objects.first()

        self.assertIsNotNone(licenciatura)
        self.assertIsInstance(licenciatura.apresentacao, str)
        self.assertNotIn('courseCode', licenciatura.apresentacao)
        self.assertTrue(TFC.objects.exists())
