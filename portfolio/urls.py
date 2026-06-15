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
    landing_page_view,
    sobre_view,
    videotutoriais_view,
    # Colega — Paintball Events API
    colega_eventos_lista,
    colega_evento_detalhe,
    colega_evento_editar,
    colega_evento_apagar,
    colega_participantes_lista,
    colega_participante_editar,
    colega_participante_apagar,
    colega_equipas_lista,
    colega_equipa_editar,
    colega_equipa_apagar,
)

urlpatterns = [
    path('', landing_page_view, name='landing_page'),
    path('home/', home, name='home'),
    path('sobre/', sobre_view, name='sobre'),
    path('videotutoriais/', videotutoriais_view, name='videotutoriais'),
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

    # ── API do Colega: Paintball Events ──
    # Events
    path('paintball/', colega_eventos_lista, name='colega_eventos_lista'),
    path('paintball/eventos/<int:evento_id>/', colega_evento_detalhe, name='colega_evento_detalhe'),
    path('paintball/eventos/<int:evento_id>/editar/', colega_evento_editar, name='colega_evento_editar'),
    path('paintball/eventos/<int:evento_id>/apagar/', colega_evento_apagar, name='colega_evento_apagar'),
    # Participants
    path('paintball/participantes/', colega_participantes_lista, name='colega_participantes_lista'),
    path('paintball/participantes/<int:participante_id>/editar/', colega_participante_editar, name='colega_participante_editar'),
    path('paintball/participantes/<int:participante_id>/apagar/', colega_participante_apagar, name='colega_participante_apagar'),
    # Teams
    path('paintball/equipas/', colega_equipas_lista, name='colega_equipas_lista'),
    path('paintball/equipas/<int:equipa_id>/editar/', colega_equipa_editar, name='colega_equipa_editar'),
    path('paintball/equipas/<int:equipa_id>/apagar/', colega_equipa_apagar, name='colega_equipa_apagar'),
]
