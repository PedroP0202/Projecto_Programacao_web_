from django.contrib import admin

from .models import Artigo, Comentario, Like, Rating


@admin.register(Artigo)
class ArtigoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'data_criacao']
    list_filter = ['data_criacao', 'autor']
    search_fields = ['titulo', 'texto', 'autor__username']
    readonly_fields = ['data_criacao']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(autor=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.autor = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if obj is not None and not request.user.is_superuser:
            return obj.autor == request.user
        return super().has_change_permission(request, obj)


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['artigo', 'autor', 'nome_autor', 'data_criacao']
    list_filter = ['data_criacao', 'autor']
    search_fields = ['texto', 'autor__username', 'nome_autor', 'artigo__titulo']
    readonly_fields = ['data_criacao']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['artigo', 'utilizador', 'session_key', 'data_criacao']
    list_filter = ['data_criacao']
    search_fields = ['artigo__titulo', 'utilizador__username', 'session_key']
    readonly_fields = ['data_criacao']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['artigo', 'valor', 'utilizador', 'session_key', 'data_criacao']
    list_filter = ['valor', 'data_criacao']
    search_fields = ['artigo__titulo', 'utilizador__username', 'session_key']
    readonly_fields = ['data_criacao']
