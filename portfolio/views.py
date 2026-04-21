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
