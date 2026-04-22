from django.urls import path

from .views import (
    competencias_view,
    formacoes_view,
    home,
    licenciatura_view,
    makingof_view,
    projetos_view,
    tecnologias_view,
)

urlpatterns = [
    path('', home, name='home'),
    path('licenciatura/', licenciatura_view, name='licenciatura'),
    path('projetos/', projetos_view, name='projetos'),
    path('tecnologias/', tecnologias_view, name='tecnologias'),
    path('competencias/', competencias_view, name='competencias'),
    path('formacoes/', formacoes_view, name='formacoes'),
    path('makingof/', makingof_view, name='makingof')
]
