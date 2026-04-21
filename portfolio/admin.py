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
)

admin.site.register([
    Licenciatura,
    Docente,
    UnidadeCurricular,
    Tecnologia,
    Projeto,
    TFC,
    Competencia,
    Formacao,
    MakingOf,
    Interesse,
])
