from django.urls import path

from . import views


app_name = 'artigos'

urlpatterns = [
    path('', views.lista_artigos, name='lista'),
    path('novo/', views.criar_artigo, name='criar'),
    path('<int:pk>/editar/', views.editar_artigo, name='editar'),
    path('<int:pk>/gostar/', views.gostar_artigo, name='gostar'),
    path('<int:pk>/comentar/', views.comentar_artigo, name='comentar'),
    path('<int:pk>/rating/', views.rating_artigo, name='rating'),
]
