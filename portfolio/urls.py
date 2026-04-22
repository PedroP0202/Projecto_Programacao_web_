from django.urls import path

from .views import (
    competencias_view,
    formacoes_view,
    home,
    licenciatura_view,
    projetos_view,
    tfcs_view,
    ucs_view,
)

urlpatterns = [
    path('', home, name='home'),
    path('licenciatura/', licenciatura_view, name='licenciatura'),
    path('ucs/', ucs_view, name='ucs'),
    path('projetos/', projetos_view, name='projetos'),
    path('competencias/', competencias_view, name='competencias'),
    path('formacoes/', formacoes_view, name='formacoes'),
    path('tfcs/', tfcs_view, name='tfcs'),
]
