from django.urls import path

from .views import (
    competencias_view,
    docentes_view,
    formacoes_view,
    home,
    interesses_view,
    licenciatura_view,
    makingof_view,
    projetos_view,
    tecnologias_view,
    tfcs_view,
    ucs_view,
)

urlpatterns = [
    path('', home, name='home'),
    path('licenciatura/', licenciatura_view, name='licenciatura'),
    path('ucs/', ucs_view, name='ucs'),
    path('projetos/', projetos_view, name='projetos'),
    path('docentes/', docentes_view, name='docentes'),
    path('tecnologias/', tecnologias_view, name='tecnologias'),
    path('competencias/', competencias_view, name='competencias'),
    path('formacoes/', formacoes_view, name='formacoes'),
    path('interesses/', interesses_view, name='interesses'),
    path('makingof/', makingof_view, name='makingof'),
    path('tfcs/', tfcs_view, name='tfcs'),
]
