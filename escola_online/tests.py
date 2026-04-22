from django.test import TestCase
from django.urls import reverse

from escola_online.models import Aluno, Curso, Professor


class EscolaModelTests(TestCase):
    def test_curso_repr_and_relationships(self):
        professor = Professor.objects.create(nome='Maria Silva', email='maria@example.com')
        aluno = Aluno.objects.create(nome='Joao', numero='A123')
        curso = Curso.objects.create(nome='Curso de Teste', professor=professor)

        curso.alunos.add(aluno)

        self.assertEqual(str(curso), 'Curso de Teste')
        self.assertEqual(curso.alunos.count(), 1)


class EscolaViewTests(TestCase):
    def test_cursos_view_loads(self):
        professor = Professor.objects.create(nome='Ana Costa', email='ana@example.com')
        aluno = Aluno.objects.create(nome='Rita', numero='A001')
        curso = Curso.objects.create(nome='Programacao Web', professor=professor)
        curso.alunos.add(aluno)

        response = self.client.get(reverse('cursos'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Programacao Web')
        self.assertContains(response, 'Ana Costa')
        self.assertContains(response, 'Rita')
