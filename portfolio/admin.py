from django.contrib import admin
from .models import (
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
    Videotutorial,
)

admin.site.register([
    Licenciatura,
    Docente,
    UnidadeCurricular,
    Tecnologia,
    Projeto,
    Competencia,
    Interesse,
    Formacao,
    TFC,
    MakingOf,
    Videotutorial,
])
