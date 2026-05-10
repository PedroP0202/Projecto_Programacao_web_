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
