from django.shortcuts import get_object_or_404
from ninja import NinjaAPI
from typing import List

from .models import Exercicio, GrupoMuscular, PlanoTreino
from .schemas import (
    ErrorSchema,
    ExercicioIn,
    ExercicioOut,
    GrupoMuscularIn,
    GrupoMuscularOut,
    PlanoTreinoIn,
    PlanoTreinoOut,
)

api = NinjaAPI(
    title="API RESTful Ginásio",
    description="API para gestão de ginásio: grupos musculares, planos e exercícios.",
    version="1.0.0",
)


# Grupos Musculares

@api.get(
    "grupos/",
    response={200: List[GrupoMuscularOut]},
    tags=["Grupos Musculares"],
    description="Lista grupos musculares (filtro por nome + paginação)",
)
def lista_grupos(request, nome: str = None, limit: int = 10, offset: int = 0):
    qs = GrupoMuscular.objects.all()
    if nome is not None:
        qs = qs.filter(nome__icontains=nome)
    qs = qs[offset:offset + limit]
    return 200, qs


@api.post(
    "grupos/",
    response={201: GrupoMuscularOut},
    tags=["Grupos Musculares"],
    description="Cria um novo grupo muscular",
)
def cria_grupo(request, data: GrupoMuscularIn):
    return 201, GrupoMuscular.objects.create(**data.dict())


@api.get(
    "grupos/{grupo_id}/",
    response={200: GrupoMuscularOut, 404: ErrorSchema},
    tags=["Grupos Musculares"],
    description="Ver um grupo muscular",
)
def ver_grupo(request, grupo_id: int):
    return 200, get_object_or_404(GrupoMuscular, id=grupo_id)


@api.put(
    "grupos/{grupo_id}/",
    response={200: GrupoMuscularOut, 404: ErrorSchema},
    tags=["Grupos Musculares"],
    description="Atualiza um grupo muscular",
)
def atualiza_grupo(request, grupo_id: int, data: GrupoMuscularIn):
    grupo = get_object_or_404(GrupoMuscular, id=grupo_id)
    for attr, value in data.dict().items():
        setattr(grupo, attr, value)
    grupo.save()
    return 200, grupo


@api.delete(
    "grupos/{grupo_id}/",
    response={204: None, 404: ErrorSchema},
    tags=["Grupos Musculares"],
    description="Remove um grupo muscular",
)
def apaga_grupo(request, grupo_id: int):
    grupo = get_object_or_404(GrupoMuscular, id=grupo_id)
    grupo.delete()
    return 204, None


# Planos de Treino

@api.get(
    "planos/",
    response={200: List[PlanoTreinoOut]},
    tags=["Planos de Treino"],
    description="Lista planos de treino (filtro por nome + paginação)",
)
def lista_planos(request, nome: str = None, limit: int = 10, offset: int = 0):
    qs = PlanoTreino.objects.all()
    if nome is not None:
        qs = qs.filter(nome__icontains=nome)
    qs = qs[offset:offset + limit]
    return 200, qs


@api.post(
    "planos/",
    response={201: PlanoTreinoOut},
    tags=["Planos de Treino"],
    description="Cria um novo plano de treino",
)
def cria_plano(request, data: PlanoTreinoIn):
    return 201, PlanoTreino.objects.create(**data.dict())


@api.get(
    "planos/{plano_id}/",
    response={200: PlanoTreinoOut, 404: ErrorSchema},
    tags=["Planos de Treino"],
    description="Ver um plano de treino",
)
def ver_plano(request, plano_id: int):
    return 200, get_object_or_404(PlanoTreino, id=plano_id)


@api.put(
    "planos/{plano_id}/",
    response={200: PlanoTreinoOut, 404: ErrorSchema},
    tags=["Planos de Treino"],
    description="Atualiza um plano de treino",
)
def atualiza_plano(request, plano_id: int, data: PlanoTreinoIn):
    plano = get_object_or_404(PlanoTreino, id=plano_id)
    for attr, value in data.dict().items():
        setattr(plano, attr, value)
    plano.save()
    return 200, plano


@api.delete(
    "planos/{plano_id}/",
    response={204: None, 404: ErrorSchema},
    tags=["Planos de Treino"],
    description="Remove um plano de treino",
)
def apaga_plano(request, plano_id: int):
    plano = get_object_or_404(PlanoTreino, id=plano_id)
    plano.delete()
    return 204, None


# Exercícios

@api.get(
    "exercicios/",
    response={200: List[ExercicioOut]},
    tags=["Exercícios"],
    description="Lista exercícios (filtros + paginação)",
)
def lista_exercicios(
    request,
    nome: str = None,
    grupo_muscular: int = None,
    limit: int = 10,
    offset: int = 0,
):
    qs = Exercicio.objects.select_related("grupo_muscular").prefetch_related("plano_treino")
    if nome is not None:
        qs = qs.filter(nome__icontains=nome)
    if grupo_muscular is not None:
        qs = qs.filter(grupo_muscular_id=grupo_muscular)
    qs = qs[offset:offset + limit]
    return 200, qs


@api.post(
    "exercicios/",
    response={201: ExercicioOut},
    tags=["Exercícios"],
    description="Cria um novo exercício",
)
def cria_exercicio(request, data: ExercicioIn):
    grupo = get_object_or_404(GrupoMuscular, id=data.grupo_muscular)
    exercicio = Exercicio.objects.create(
        nome=data.nome,
        descricao=data.descricao,
        grupo_muscular=grupo,
    )
    exercicio.plano_treino.set(data.plano_treino)
    return 201, exercicio


@api.get(
    "exercicios/{exercicio_id}/",
    response={200: ExercicioOut, 404: ErrorSchema},
    tags=["Exercícios"],
    description="Ver um exercício",
)
def ver_exercicio(request, exercicio_id: int):
    return 200, get_object_or_404(Exercicio, id=exercicio_id)


@api.put(
    "exercicios/{exercicio_id}/",
    response={200: ExercicioOut, 404: ErrorSchema},
    tags=["Exercícios"],
    description="Atualiza um exercício",
)
def atualiza_exercicio(request, exercicio_id: int, data: ExercicioIn):
    exercicio = get_object_or_404(Exercicio, id=exercicio_id)
    grupo = get_object_or_404(GrupoMuscular, id=data.grupo_muscular)
    exercicio.nome = data.nome
    exercicio.descricao = data.descricao
    exercicio.grupo_muscular = grupo
    exercicio.save()
    exercicio.plano_treino.set(data.plano_treino)
    return 200, exercicio


@api.delete(
    "exercicios/{exercicio_id}/",
    response={204: None, 404: ErrorSchema},
    tags=["Exercícios"],
    description="Remove um exercício",
)
def apaga_exercicio(request, exercicio_id: int):
    exercicio = get_object_or_404(Exercicio, id=exercicio_id)
    exercicio.delete()
    return 204, None
