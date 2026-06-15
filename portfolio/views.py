import os

import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from accounts.utils import user_is_portfolio_manager

from .forms import (
    CompetenciaForm,
    DocenteForm,
    FormacaoForm,
    InteresseForm,
    LicenciaturaForm,
    MakingOfForm,
    ProjetoForm,
    TecnologiaForm,
    TFCForm,
    UnidadeCurricularForm,
)
from .models import (
    Competencia,
    Docente,
    Formacao,
    Interesse,
    Licenciatura,
    MakingOf,
    Projeto,
    Tecnologia,
    TFC,
    UnidadeCurricular,
    Videotutorial,
)


PORTFOLIO_CRUD = {
    'licenciaturas': {
        'model': Licenciatura,
        'form': LicenciaturaForm,
        'name': 'Licenciatura',
        'success_url': 'licenciatura',
    },
    'disciplinas': {
        'model': UnidadeCurricular,
        'form': UnidadeCurricularForm,
        'name': 'Disciplina',
        'success_url': 'ucs',
    },
    'docentes': {
        'model': Docente,
        'form': DocenteForm,
        'name': 'Docente',
        'success_url': 'docentes',
    },
    'projetos': {
        'model': Projeto,
        'form': ProjetoForm,
        'name': 'Projeto',
        'success_url': 'projetos',
    },
    'tecnologias': {
        'model': Tecnologia,
        'form': TecnologiaForm,
        'name': 'Tecnologia',
        'success_url': 'tecnologias',
    },
    'competencias': {
        'model': Competencia,
        'form': CompetenciaForm,
        'name': 'Competência',
        'success_url': 'competencias',
    },
    'interesses': {
        'model': Interesse,
        'form': InteresseForm,
        'name': 'Interesse',
        'success_url': 'interesses',
    },
    'formacoes': {
        'model': Formacao,
        'form': FormacaoForm,
        'name': 'Formação',
        'success_url': 'formacoes',
    },
    'tfcs': {
        'model': TFC,
        'form': TFCForm,
        'name': 'TFC',
        'success_url': 'tfcs',
    },
    'makingof': {
        'model': MakingOf,
        'form': MakingOfForm,
        'name': 'Making Of',
        'success_url': 'makingof',
    },
}


portfolio_manager_required = user_passes_test(user_is_portfolio_manager)


def home(request):
    licenciatura = Licenciatura.objects.first()
    projetos = Projeto.objects.select_related('unidade_curricular').prefetch_related('tecnologias').order_by('nome')
    competencias = Competencia.objects.order_by('categoria', 'titulo')
    formacoes = Formacao.objects.order_by('-data_inicio')

    context = {
        'licenciatura': licenciatura,
        'projetos': projetos[:6],
        'competencias': competencias[:8],
        'total_projetos': projetos.count(),
        'total_competencias': competencias.count(),
        'total_formacoes': formacoes.count(),
    }
    return render(request, 'portfolio/home.html', context)


def licenciatura_view(request):
    licenciatura = Licenciatura.objects.first()
    disciplinas = UnidadeCurricular.objects.order_by('ano', 'semestre', 'nome')
    return render(
        request,
        'portfolio/licenciatura.html',
        {
            'licenciatura': licenciatura,
            'disciplinas': disciplinas,
        },
    )




def projetos_view(request):
    projetos = Projeto.objects.select_related('unidade_curricular').prefetch_related('tecnologias').order_by('nome')
    return render(request, 'portfolio/projetos.html', {'projetos': projetos})


def competencias_view(request):
    competencias = Competencia.objects.order_by('categoria', 'titulo')
    return render(request, 'portfolio/competencias.html', {'competencias': competencias})


def formacoes_view(request):
    formacoes = Formacao.objects.order_by('-data_inicio')
    return render(request, 'portfolio/formacoes.html', {'formacoes': formacoes})


def ucs_view(request):
    disciplinas = UnidadeCurricular.objects.select_related('licenciatura').prefetch_related('docentes').order_by('ano', 'semestre', 'nome')
    return render(request, 'portfolio/ucs.html', {'disciplinas': disciplinas})


def docentes_view(request):
    docentes = Docente.objects.prefetch_related('ucs').order_by('nome')
    return render(request, 'portfolio/docentes.html', {'docentes': docentes})




def tecnologias_view(request):
    tecnologias = Tecnologia.objects.prefetch_related('projetos').order_by('nome')
    return render(request, 'portfolio/tecnologias.html', {'tecnologias': tecnologias})


def interesses_view(request):
    interesses = Interesse.objects.order_by('titulo')
    return render(request, 'portfolio/interesses.html', {'interesses': interesses})


def tfcs_view(request):
    tfcs = TFC.objects.order_by('-ano', 'titulo')
    return render(request, 'portfolio/tfcs.html', {'tfcs': tfcs})


def makingof_view(request):
    registos = MakingOf.objects.order_by('-data')
    return render(request, 'portfolio/makingof.html', {'registos': registos})


@login_required
@portfolio_manager_required
def portfolio_create(request, model_slug):
    config = get_crud_config(model_slug)
    form_class = config['form']

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f"{config['name']} criado com sucesso.")
            return redirect(config['success_url'])
    else:
        form = form_class()

    return render(
        request,
        'portfolio/object_form.html',
        {
            'form': form,
            'title': f"Criar {config['name']}",
            'cancel_url': config['success_url'],
        },
    )


@login_required
@portfolio_manager_required
def portfolio_update(request, model_slug, pk):
    config = get_crud_config(model_slug)
    obj = get_object_or_404(config['model'], pk=pk)
    form_class = config['form']

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, f"{config['name']} atualizado com sucesso.")
            return redirect(config['success_url'])
    else:
        form = form_class(instance=obj)

    return render(
        request,
        'portfolio/object_form.html',
        {
            'form': form,
            'title': f"Editar {config['name']}",
            'cancel_url': config['success_url'],
        },
    )


@login_required
@portfolio_manager_required
def portfolio_delete(request, model_slug, pk):
    config = get_crud_config(model_slug)
    obj = get_object_or_404(config['model'], pk=pk)

    if request.method == 'POST':
        obj.delete()
        messages.success(request, f"{config['name']} apagado com sucesso.")
        return redirect(config['success_url'])

    return render(
        request,
        'portfolio/object_confirm_delete.html',
        {
            'object': obj,
            'title': f"Apagar {config['name']}",
            'cancel_url': config['success_url'],
        },
    )


def get_crud_config(model_slug):
    try:
        return PORTFOLIO_CRUD[model_slug]
    except KeyError as exc:
        raise Http404('Tipo de conteúdo não encontrado.') from exc


def landing_page_view(request):
    return render(request, 'portfolio/landing_page.html')


def sobre_view(request):
    return render(request, 'portfolio/sobre.html')


def videotutoriais_view(request):
    videotutoriais = Videotutorial.objects.all()
    return render(request, 'portfolio/videotutoriais.html', {'videotutoriais': videotutoriais})


# ──────────────────────────────────────────────
# Helpers para consumir a API do Colega (Paintball Events)
# ──────────────────────────────────────────────

COLEGA_SWAGGER_URL = "https://paintball-events-api.pw.deisi.ulusofona.pt/api/docs"


def _colega_headers():
    """Devolve os headers com a API Key do colega lida do .env."""
    return {"X-API-Key": os.environ.get("COLEGA_API_KEY", "")}


def _colega_url(path=""):
    """Devolve o URL base da API do colega + path."""
    base = os.environ.get("COLEGA_API_URL", "https://paintball-events-api.pw.deisi.ulusofona.pt/api").rstrip("/")
    return f"{base}{path}"


def _api_get(path, params=None):
    """Faz GET à API do colega e devolve (dados, erro)."""
    try:
        r = requests.get(_colega_url(path), params=params, headers=_colega_headers(), timeout=10)
        if r.status_code == 200:
            return r.json(), None
        return None, f"Erro {r.status_code}: {r.text}"
    except requests.exceptions.RequestException as e:
        return None, f"Não foi possível conectar à API do colega: {e}"


# ════════════════════════════════════
# EVENTS
# ════════════════════════════════════

def colega_eventos_lista(request):
    pesquisa = request.GET.get("pesquisa", "")
    location = request.GET.get("location", "")
    order_by = request.GET.get("order_by", "name")
    limit = int(request.GET.get("limit", 10))
    offset = int(request.GET.get("offset", 0))

    params = {"search": pesquisa, "location": location, "order_by": order_by,
              "limit": limit, "offset": offset}

    if request.method == "POST":
        payload = {
            "name": request.POST.get("name", ""),
            "date": request.POST.get("date", ""),
            "location": request.POST.get("location", ""),
            "price": request.POST.get("price", "0"),
            "description": request.POST.get("description", ""),
        }
        try:
            r = requests.post(_colega_url("/events"), json=payload, headers=_colega_headers(), timeout=10)
            if r.status_code in (200, 201):
                messages.success(request, "Evento criado com sucesso!")
                return redirect("colega_eventos_lista")
            else:
                messages.error(request, f"Erro ao criar evento: {r.status_code} – {r.text}")
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Sem ligação à API: {e}")

    dados, erro = _api_get("/events", params)
    return render(request, "portfolio/colega_eventos_lista.html", {
        "dados": dados, "erro": erro,
        "pesquisa": pesquisa, "location": location, "order_by": order_by,
        "limit": limit, "offset": offset,
        "swagger_url": COLEGA_SWAGGER_URL,
    })


def colega_evento_detalhe(request, evento_id):
    dados, erro = _api_get(f"/events/{evento_id}")
    participantes, _ = _api_get("/participants", {"event_id": evento_id, "limit": 50})
    return render(request, "portfolio/colega_evento_detalhe.html", {
        "dados": dados, "erro": erro,
        "participantes": participantes,
        "evento_id": evento_id,
    })


def colega_evento_editar(request, evento_id):
    if request.method == "POST":
        payload = {
            "name": request.POST.get("name", ""),
            "date": request.POST.get("date", ""),
            "location": request.POST.get("location", ""),
            "price": request.POST.get("price", "0"),
            "description": request.POST.get("description", ""),
        }
        try:
            r = requests.put(_colega_url(f"/events/{evento_id}"), json=payload,
                             headers=_colega_headers(), timeout=10)
            if r.status_code == 200:
                messages.success(request, "Evento atualizado com sucesso!")
                return redirect("colega_evento_detalhe", evento_id=evento_id)
            else:
                messages.error(request, f"Erro ao atualizar: {r.status_code} – {r.text}")
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Sem ligação à API: {e}")

    dados, erro = _api_get(f"/events/{evento_id}")
    return render(request, "portfolio/colega_evento_form.html", {
        "dados": dados, "erro": erro, "evento_id": evento_id, "modo": "editar",
    })


def colega_evento_apagar(request, evento_id):
    if request.method == "POST":
        try:
            r = requests.delete(_colega_url(f"/events/{evento_id}"),
                                headers=_colega_headers(), timeout=10)
            if r.status_code in (200, 204):
                messages.success(request, "Evento apagado com sucesso!")
                return redirect("colega_eventos_lista")
            else:
                messages.error(request, f"Erro ao apagar: {r.status_code} – {r.text}")
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Sem ligação à API: {e}")

    dados, erro = _api_get(f"/events/{evento_id}")
    return render(request, "portfolio/colega_evento_apagar.html", {
        "dados": dados, "erro": erro, "evento_id": evento_id,
    })


# ════════════════════════════════════
# PARTICIPANTS
# ════════════════════════════════════

def colega_participantes_lista(request):
    pesquisa = request.GET.get("pesquisa", "")
    event_id = request.GET.get("event_id", "")
    order_by = request.GET.get("order_by", "name")
    limit = int(request.GET.get("limit", 10))
    offset = int(request.GET.get("offset", 0))

    params = {"search": pesquisa, "order_by": order_by, "limit": limit, "offset": offset}
    if event_id:
        params["event_id"] = event_id

    if request.method == "POST":
        payload = {
            "name": request.POST.get("name", ""),
            "email": request.POST.get("email", ""),
            "age": int(request.POST.get("age", 18)),
            "event_id": int(request.POST.get("event_id", 1)),
        }
        try:
            r = requests.post(_colega_url("/participants"), json=payload,
                              headers=_colega_headers(), timeout=10)
            if r.status_code in (200, 201):
                messages.success(request, "Participante criado com sucesso!")
                return redirect("colega_participantes_lista")
            else:
                messages.error(request, f"Erro ao criar participante: {r.status_code} – {r.text}")
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Sem ligação à API: {e}")

    dados, erro = _api_get("/participants", params)
    eventos, _ = _api_get("/events", {"limit": 100})
    return render(request, "portfolio/colega_participantes_lista.html", {
        "dados": dados, "erro": erro,
        "pesquisa": pesquisa, "event_id": event_id, "order_by": order_by,
        "limit": limit, "offset": offset,
        "eventos": eventos,
        "swagger_url": COLEGA_SWAGGER_URL,
    })


def colega_participante_editar(request, participante_id):
    if request.method == "POST":
        payload = {
            "name": request.POST.get("name", ""),
            "email": request.POST.get("email", ""),
            "age": int(request.POST.get("age", 18)),
            "event_id": int(request.POST.get("event_id", 1)),
        }
        try:
            r = requests.put(_colega_url(f"/participants/{participante_id}"), json=payload,
                             headers=_colega_headers(), timeout=10)
            if r.status_code == 200:
                messages.success(request, "Participante atualizado!")
                return redirect("colega_participantes_lista")
            else:
                messages.error(request, f"Erro: {r.status_code} – {r.text}")
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Sem ligação à API: {e}")

    dados, erro = _api_get(f"/participants/{participante_id}")
    eventos, _ = _api_get("/events", {"limit": 100})
    return render(request, "portfolio/colega_participante_form.html", {
        "dados": dados, "erro": erro,
        "participante_id": participante_id,
        "eventos": eventos,
        "modo": "editar",
    })


def colega_participante_apagar(request, participante_id):
    if request.method == "POST":
        try:
            r = requests.delete(_colega_url(f"/participants/{participante_id}"),
                                headers=_colega_headers(), timeout=10)
            if r.status_code in (200, 204):
                messages.success(request, "Participante apagado!")
                return redirect("colega_participantes_lista")
            else:
                messages.error(request, f"Erro: {r.status_code} – {r.text}")
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Sem ligação à API: {e}")

    dados, erro = _api_get(f"/participants/{participante_id}")
    return render(request, "portfolio/colega_participante_apagar.html", {
        "dados": dados, "erro": erro, "participante_id": participante_id,
    })


# ════════════════════════════════════
# TEAMS
# ════════════════════════════════════

def colega_equipas_lista(request):
    pesquisa = request.GET.get("pesquisa", "")
    color = request.GET.get("color", "")
    order_by = request.GET.get("order_by", "name")
    limit = int(request.GET.get("limit", 10))
    offset = int(request.GET.get("offset", 0))

    params = {"search": pesquisa, "color": color, "order_by": order_by,
              "limit": limit, "offset": offset}

    if request.method == "POST":
        payload = {
            "name": request.POST.get("name", ""),
            "color": request.POST.get("color", ""),
            "participant_ids": [
                int(x) for x in request.POST.getlist("participant_ids") if x
            ],
        }
        try:
            r = requests.post(_colega_url("/teams"), json=payload,
                              headers=_colega_headers(), timeout=10)
            if r.status_code in (200, 201):
                messages.success(request, "Equipa criada com sucesso!")
                return redirect("colega_equipas_lista")
            else:
                messages.error(request, f"Erro ao criar equipa: {r.status_code} – {r.text}")
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Sem ligação à API: {e}")

    dados, erro = _api_get("/teams", params)
    return render(request, "portfolio/colega_equipas_lista.html", {
        "dados": dados, "erro": erro,
        "pesquisa": pesquisa, "color": color, "order_by": order_by,
        "limit": limit, "offset": offset,
        "swagger_url": COLEGA_SWAGGER_URL,
    })


def colega_equipa_editar(request, equipa_id):
    if request.method == "POST":
        payload = {
            "name": request.POST.get("name", ""),
            "color": request.POST.get("color", ""),
            "participant_ids": [
                int(x) for x in request.POST.getlist("participant_ids") if x
            ],
        }
        try:
            r = requests.put(_colega_url(f"/teams/{equipa_id}"), json=payload,
                             headers=_colega_headers(), timeout=10)
            if r.status_code == 200:
                messages.success(request, "Equipa atualizada!")
                return redirect("colega_equipas_lista")
            else:
                messages.error(request, f"Erro: {r.status_code} – {r.text}")
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Sem ligação à API: {e}")

    dados, erro = _api_get(f"/teams/{equipa_id}")
    participantes, _ = _api_get("/participants", {"limit": 100})
    return render(request, "portfolio/colega_equipa_form.html", {
        "dados": dados, "erro": erro,
        "equipa_id": equipa_id,
        "participantes": participantes,
        "modo": "editar",
    })


def colega_equipa_apagar(request, equipa_id):
    if request.method == "POST":
        try:
            r = requests.delete(_colega_url(f"/teams/{equipa_id}"),
                                headers=_colega_headers(), timeout=10)
            if r.status_code in (200, 204):
                messages.success(request, "Equipa apagada!")
                return redirect("colega_equipas_lista")
            else:
                messages.error(request, f"Erro: {r.status_code} – {r.text}")
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Sem ligação à API: {e}")

    dados, erro = _api_get(f"/teams/{equipa_id}")
    return render(request, "portfolio/colega_equipa_apagar.html", {
        "dados": dados, "erro": erro, "equipa_id": equipa_id,
    })

