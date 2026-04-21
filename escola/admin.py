from django.contrib import admin
from .models import Aluno, Curso, Professor

admin.site.register([Professor, Aluno, Curso])
