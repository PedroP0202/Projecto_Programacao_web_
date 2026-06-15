from django.contrib import admin

from .models import APIKey, Exercicio, GrupoMuscular, PlanoTreino


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('name', 'key', 'is_active', 'expiration_date', 'created_at')
    list_filter = ('is_active',)
    readonly_fields = ('key', 'created_at')
    search_fields = ('name',)


admin.site.register(GrupoMuscular)
admin.site.register(PlanoTreino)
admin.site.register(Exercicio)
