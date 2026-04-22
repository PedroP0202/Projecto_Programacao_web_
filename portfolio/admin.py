from django.contrib import admin
from .models import (
    Competencia,
    Docente,
    Formacao,
    Licenciatura,
    MakingOf,
    Projeto,
    Tecnologia,

)

admin.site.register([
    Licenciatura,
    Docente,
    Tecnologia,
    Projeto,
    Competencia,
    Formacao,
    MakingOf,
])
