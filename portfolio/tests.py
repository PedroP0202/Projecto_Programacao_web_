import os
from io import StringIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from portfolio.models import (
    Competencia,
    Docente,
    Formacao,
    Interesse,
    Licenciatura,
    MakingOf,
    Projeto,
    Tecnologia,
    TFC,
    UnidadeCurricular,
)

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

    def test_portfolio_section_pages_load(self):
        Licenciatura.objects.create(
            nome='Engenharia Informática',
            apresentacao='Curso simples e funcional.',
            objetivos='Aprender a programar.',
            competencias='Python, Django e bases de dados.',
            saidas_profissionais='Desenvolvimento de software.',
        )
        docente = Docente.objects.create(
            nome='Professor Teste',
            link_lusofona='https://example.com/docente',
        )
        uc = UnidadeCurricular.objects.create(
            nome='Programacao',
            sigla='PW',
            ano=2,
            semestre=1,
            creditos=6,
            licenciatura=Licenciatura.objects.first(),
        )
        uc.docentes.add(docente)
        tecnologia = Tecnologia.objects.create(
            nome='Python',
            link_oficial='https://python.org',
            descricao='Linguagem',
            nivel_interesse=4,
        )
        projeto = Projeto.objects.create(
            nome='Projeto Teste',
            descricao='Descricao do projeto.',
            conceitos_aplicados='MVC',
            unidade_curricular=uc,
        )
        projeto.tecnologias.add(tecnologia)
        Competencia.objects.create(
            titulo='Django',
            categoria='Hard Skill',
            descricao='Framework web.',
            nivel=3,
        )
        Formacao.objects.create(
            titulo='Curso Django',
            instituicao='ULHT',
            data_inicio='2024-01-01',
            descricao='Formacao base.',
            local='Lisboa',
        )
        TFC.objects.create(
            titulo='TFC Teste',
            autores='Aluno',
            orientadores='Professor',
            ano=2025,
            resumo='Resumo de teste.',
        )
        Interesse.objects.create(
            titulo='IA',
            descricao='Interesse em inteligencia artificial.',
        )
        MakingOf.objects.create(
            titulo='Registo',
            descricao='Descricao',
            decisoes_tomadas='Decisoes',
            erros_e_correcoes='Correcao',
            uso_ia='Sim',
        )

        for route_name in [
            'licenciatura',
            'ucs',
            'docentes',
            'projetos',
            'tecnologias',
            'competencias',
            'formacoes',
            'interesses',
            'makingof',
            'tfcs',
        ]:
            response = self.client.get(reverse(route_name))
            self.assertEqual(response.status_code, 200, route_name)


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
