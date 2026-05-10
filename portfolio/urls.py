from django.urls import path

from .views import (
    competencias_view,
    docentes_view,
    formacoes_view,
    home,
    interesses_view,
    licenciatura_view,
    makingof_view,
    portfolio_create,
    portfolio_delete,
    portfolio_update,
    projetos_view,
    tecnologias_view,
    tfcs_view,
    ucs_view,
)

urlpatterns = [
    path('', home, name='home'),
    path('licenciatura/', licenciatura_view, name='licenciatura'),
    path('ucs/', ucs_view, name='ucs'),
    path('docentes/', docentes_view, name='docentes'),
    path('projetos/', projetos_view, name='projetos'),
    path('tecnologias/', tecnologias_view, name='tecnologias'),
    path('competencias/', competencias_view, name='competencias'),
    path('formacoes/', formacoes_view, name='formacoes'),
    path('interesses/', interesses_view, name='interesses'),
    path('tfcs/', tfcs_view, name='tfcs'),
    path('makingof/', makingof_view, name='makingof'),
    path('gestao/<str:model_slug>/novo/', portfolio_create, name='portfolio_create'),
    path('gestao/<str:model_slug>/<int:pk>/editar/', portfolio_update, name='portfolio_update'),
    path('gestao/<str:model_slug>/<int:pk>/apagar/', portfolio_delete, name='portfolio_delete'),
]
