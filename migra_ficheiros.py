import os
from pathlib import Path

from django.conf import settings
from django.core.files import File

from artigos.models import Artigo
from escola_online.models import Curso
from portfolio.models import (
    Interesse,
    MakingOf,
    Projeto,
    Tecnologia,
    TFC,
    UnidadeCurricular,
)


MODELOS_COM_IMAGENS = [
    (UnidadeCurricular, 'imagem'),
    (Tecnologia, 'logo'),
    (Projeto, 'imagem'),
    (Interesse, 'imagem'),
    (TFC, 'imagem'),
    (MakingOf, 'imagem_caderno'),
    (Artigo, 'fotografia'),
    (Curso, 'imagem'),
]


def caminho_local(nome_ficheiro):
    media_root = Path(settings.MEDIA_ROOT)
    candidatos = [
        media_root / nome_ficheiro,
        Path(settings.BASE_DIR) / nome_ficheiro,
    ]

    for candidato in candidatos:
        if candidato.exists():
            return candidato

    return media_root / nome_ficheiro


def migrar_ficheiro(obj, campo_nome):
    campo = getattr(obj, campo_nome)
    if not campo or not campo.name:
        return 'sem_ficheiro'

    local_path = caminho_local(campo.name)
    if not os.path.exists(local_path):
        print(f'Ignorado, ficheiro local nao encontrado: {obj} ({campo.name})')
        return 'nao_encontrado'

    with open(local_path, 'rb') as ficheiro:
        campo.save(
            os.path.basename(local_path),
            File(ficheiro),
            save=True,
        )

    print(f'Migrado: {obj} ({campo_nome})')
    return 'migrado'


def migrar():
    resultados = {
        'migrado': 0,
        'sem_ficheiro': 0,
        'nao_encontrado': 0,
    }

    for modelo, campo_nome in MODELOS_COM_IMAGENS:
        for obj in modelo.objects.all():
            resultado = migrar_ficheiro(obj, campo_nome)
            resultados[resultado] += 1

    print(
        'Resumo: '
        f'{resultados["migrado"]} migrados, '
        f'{resultados["sem_ficheiro"]} sem ficheiro, '
        f'{resultados["nao_encontrado"]} nao encontrados.'
    )


migrar()
