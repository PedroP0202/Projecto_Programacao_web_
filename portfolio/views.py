from django.shortcuts import render
from .models import Competencia, Formacao, Licenciatura, Projeto, TFC, UnidadeCurricular


def home(request):
    licenciatura = Licenciatura.objects.first()
    ucs = UnidadeCurricular.objects.prefetch_related('docentes').order_by('ano', 'semestre', 'nome')
    projetos = Projeto.objects.select_related('unidade_curricular').prefetch_related('tecnologias').order_by('nome')
    competencias = Competencia.objects.order_by('categoria', 'titulo')
    formacoes = Formacao.objects.order_by('-data_inicio')
    tfcs = TFC.objects.filter(destaque=True).order_by('-ano', 'titulo')

    context = {
        'licenciatura': licenciatura,
        'ucs': ucs[:8],
        'projetos': projetos[:6],
        'competencias': competencias[:8],
        'formacoes': formacoes[:5],
        'tfcs': tfcs[:5],
        'total_ucs': ucs.count(),
        'total_projetos': projetos.count(),
        'total_competencias': competencias.count(),
        'total_formacoes': formacoes.count(),
    }
    return render(request, 'portfolio/home.html', context)


def licenciatura_view(request):
    licenciatura = Licenciatura.objects.first()
    return render(request, 'portfolio/licenciatura.html', {'licenciatura': licenciatura})


def ucs_view(request):
    ucs = UnidadeCurricular.objects.select_related('licenciatura').prefetch_related('docentes').order_by(
        'ano', 'semestre', 'nome'
    )
    return render(request, 'portfolio/ucs.html', {'ucs': ucs})


def projetos_view(request):
    projetos = Projeto.objects.select_related('unidade_curricular').prefetch_related('tecnologias').order_by('nome')
    return render(request, 'portfolio/projetos.html', {'projetos': projetos})


def competencias_view(request):
    competencias = Competencia.objects.order_by('categoria', 'titulo')
    return render(request, 'portfolio/competencias.html', {'competencias': competencias})


def formacoes_view(request):
    formacoes = Formacao.objects.order_by('-data_inicio')
    return render(request, 'portfolio/formacoes.html', {'formacoes': formacoes})


def tfcs_view(request):
    tfcs = TFC.objects.order_by('-ano', 'titulo')
    return render(request, 'portfolio/tfcs.html', {'tfcs': tfcs})
