from django.contrib import admin

from .models import Exercicio, GrupoMuscular, PlanoTreino


admin.site.register(GrupoMuscular)
admin.site.register(PlanoTreino)
admin.site.register(Exercicio)
