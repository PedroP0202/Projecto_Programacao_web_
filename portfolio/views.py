from django.shortcuts import render
from .models import (
    Competencia,
    Formacao,
    Licenciatura,
    MakingOf,
    Projeto,
    Tecnologia,
)


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
    return render(request, 'portfolio/licenciatura.html', {'licenciatura': licenciatura})




def projetos_view(request):
    projetos = Projeto.objects.select_related('unidade_curricular').prefetch_related('tecnologias').order_by('nome')
    return render(request, 'portfolio/projetos.html', {'projetos': projetos})


def competencias_view(request):
    competencias = Competencia.objects.order_by('categoria', 'titulo')
    return render(request, 'portfolio/competencias.html', {'competencias': competencias})


def formacoes_view(request):
    formacoes = Formacao.objects.order_by('-data_inicio')
    return render(request, 'portfolio/formacoes.html', {'formacoes': formacoes})







def tecnologias_view(request):
    tecnologias = Tecnologia.objects.prefetch_related('projetos').order_by('nome')
    return render(request, 'portfolio/tecnologias.html', {'tecnologias': tecnologias})


def interesses_view(request):
    interesses = Interesse.objects.order_by('titulo')
    return render(request, 'portfolio/interesses.html', {'interesses': interesses})


def makingof_view(request):
    registos = MakingOf.objects.order_by('-data')
    return render(request, 'portfolio/makingof.html', {'registos': registos})
