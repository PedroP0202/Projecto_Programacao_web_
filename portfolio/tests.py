from django.test import TestCase
from django.urls import reverse

from .models import Licenciatura

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
