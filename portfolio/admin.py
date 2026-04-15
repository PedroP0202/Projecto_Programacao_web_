from django.contrib import admin
from .models import Licenciatura, Docente, UnidadeCurricular, Tecnologia, Projeto

@admin.register(Licenciatura)
class LicenciaturaAdmin(admin.ModelAdmin):
    list_display = ('nome',)

@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'link_lusofona')

@admin.register(UnidadeCurricular)
class UnidadeCurricularAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sigla', 'ano', 'semestre', 'creditos')
    list_filter = ('ano', 'semestre', 'licenciatura')
    search_fields = ('nome', 'sigla')

@admin.register(Tecnologia)
class TecnologiaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'nivel_interesse')
    list_filter = ('nivel_interesse',)

@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'unidade_curricular')
    list_filter = ('unidade_curricular',)
