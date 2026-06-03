from ninja import Schema
from typing import List


class GrupoMuscularIn(Schema):
    nome: str


class GrupoMuscularOut(Schema):
    id: int
    nome: str


class PlanoTreinoIn(Schema):
    nome: str
    descricao: str = ""


class PlanoTreinoOut(Schema):
    id: int
    nome: str
    descricao: str


class ExercicioIn(Schema):
    nome: str
    descricao: str = ""
    grupo_muscular: int
    plano_treino: List[int] = []


class ExercicioOut(Schema):
    id: int
    nome: str
    descricao: str
    grupo_muscular: GrupoMuscularOut
    plano_treino: List[PlanoTreinoOut] = []

    class Config:
        from_attributes = True


class ErrorSchema(Schema):
    detail: str
