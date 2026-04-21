from django.test import TestCase
from .models import Aluno, Curso, Professor


class EscolaModelTests(TestCase):
    def test_curso_repr_and_relationships(self):
        professor = Professor.objects.create(nome='Maria Silva', email='maria@example.com')
        aluno = Aluno.objects.create(nome='Joao', numero='A123')
        curso = Curso.objects.create(nome='Curso de Teste', professor=professor)

        curso.alunos.add(aluno)

        self.assertEqual(str(curso), 'Curso de Teste')
        self.assertEqual(curso.alunos.count(), 1)
