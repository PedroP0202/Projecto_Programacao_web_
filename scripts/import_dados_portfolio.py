"""
Script de importação de dados iniciais do portfólio pessoal.
Preenche Tecnologias, Projetos, Competências, Formações e Interesses.
Adaptado do padrão descrito em: https://github.com/ULHT-PW/importar-json

Para executar:
    python manage.py shell < scripts/import_dados_portfolio.py
ou:
    python scripts/import_dados_portfolio.py
"""

import os
import sys
import django
from datetime import date

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from portfolio.models import (
    Licenciatura, UnidadeCurricular, Tecnologia,
    Projeto, TFC, Competencia, Formacao, Interesse
)

print("=== Limpando dados parciais de modelos pessoais ===")
Tecnologia.objects.all().delete()
Competencia.objects.all().delete()
Formacao.objects.all().delete()
Interesse.objects.all().delete()
Projeto.objects.all().delete()

# =========================================================
# TECNOLOGIAS
# =========================================================
print("\n=== A importar Tecnologias ===")

tecnologias_data = [
    {
        'nome': 'Python',
        'link_oficial': 'https://www.python.org',
        'descricao': 'Linguagem de programação de alto nível, versátil e amplamente utilizada em desenvolvimento web, ciência de dados e automação.',
        'nivel_interesse': 5,
    },
    {
        'nome': 'Django',
        'link_oficial': 'https://www.djangoproject.com',
        'descricao': 'Framework web em Python que incentiva o desenvolvimento rápido e design pragmático. Usado neste portfólio.',
        'nivel_interesse': 5,
    },
    {
        'nome': 'HTML5',
        'link_oficial': 'https://developer.mozilla.org/en-US/docs/Web/HTML',
        'descricao': 'Linguagem de marcação base da web para estruturação de conteúdo.',
        'nivel_interesse': 4,
    },
    {
        'nome': 'CSS3',
        'link_oficial': 'https://developer.mozilla.org/en-US/docs/Web/CSS',
        'descricao': 'Linguagem de estilos para definição visual de páginas web. Inclui Flexbox, Grid e animações.',
        'nivel_interesse': 4,
    },
    {
        'nome': 'JavaScript',
        'link_oficial': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript',
        'descricao': 'Linguagem de programação da web para adicionar interatividade e dinamismo às páginas.',
        'nivel_interesse': 4,
    },
    {
        'nome': 'Java',
        'link_oficial': 'https://www.java.com',
        'descricao': 'Linguagem orientada a objetos amplamente utilizada em desenvolvimento empresarial e mobile (Android).',
        'nivel_interesse': 3,
    },
    {
        'nome': 'C',
        'link_oficial': 'https://en.wikipedia.org/wiki/C_(programming_language)',
        'descricao': 'Linguagem de programação de baixo nível fundamental para sistemas operativos e software embarcado.',
        'nivel_interesse': 3,
    },
    {
        'nome': 'SQL / SQLite',
        'link_oficial': 'https://www.sqlite.org',
        'descricao': 'Linguagem de consulta para bases de dados relacionais. SQLite usado no desenvolvimento do portfólio.',
        'nivel_interesse': 4,
    },
    {
        'nome': 'Git',
        'link_oficial': 'https://git-scm.com',
        'descricao': 'Sistema de controlo de versões distribuído. Essencial para colaboração e rastreamento de código.',
        'nivel_interesse': 5,
    },
    {
        'nome': 'Linux',
        'link_oficial': 'https://www.linux.org',
        'descricao': 'Sistema operativo open-source. Utilizado no contexto de Sistemas Operativos e desenvolvimento backend.',
        'nivel_interesse': 3,
    },
]

tecnologias_obj = {}
for t in tecnologias_data:
    obj, _ = Tecnologia.objects.get_or_create(nome=t['nome'], defaults=t)
    tecnologias_obj[t['nome']] = obj
    print(f"  ✓ {obj.nome}")

# =========================================================
# PROJETOS (ligados às UCs importadas)
# =========================================================
print("\n=== A importar Projetos ===")

# Obter UCs por sigla (código numérico da UC)
def get_uc(sigla):
    try:
        return UnidadeCurricular.objects.filter(sigla=sigla).first()
    except UnidadeCurricular.DoesNotExist:
        return None

projetos_data = [
    {
        'nome': 'Portfólio Web Pessoal',
        'descricao': 'Aplicação web desenvolvida em Django para apresentação do percurso académico e projetos, servindo como cartão de visitas digital.',
        'conceitos_aplicados': 'Framework Django, ORM, Templates, Admin Interface, Migrações, MVC, HTML/CSS, Media Files',
        'sigla_uc': '11195',  # Programação Web
        'tecnologias': ['Python', 'Django', 'HTML5', 'CSS3', 'SQL / SQLite'],
        'repositorio_git': 'https://github.com/pedropiedade/portfolio',
        'url_deploy': 'https://pedropiedade.pythonanywhere.com',
    },
    {
        'nome': 'Sistema de Gestão de Biblioteca',
        'descricao': 'Aplicação de gestão de livros, autores e empréstimos com interface web básica em Django. Desenvolvida para a UC de Bases de Dados.',
        'conceitos_aplicados': 'Modelação relacional, ForeignKey, ManyToMany, Django ORM, querys SQL, normalização',
        'sigla_uc': '1792',  # Bases de Dados
        'tecnologias': ['Python', 'Django', 'SQL / SQLite'],
        'repositorio_git': 'https://github.com/pedropiedade/biblioteca-django',
        'url_deploy': '',
    },
    {
        'nome': 'Jogo da Forca em Java',
        'descricao': 'Jogo da forca em modo texto implementado em Java com POO. Permite escolher categorias de palavras e tem sistema de pontuação.',
        'conceitos_aplicados': 'Programação orientada a objetos, herança, polimorfismo, encapsulamento, ArrayList, exceções',
        'sigla_uc': '898',  # Linguagens de Programação II
        'tecnologias': ['Java'],
        'repositorio_git': 'https://github.com/pedropiedade/jogo-forca-java',
        'url_deploy': '',
    },
    {
        'nome': 'Simulador de Mundo — DeisiWorld',
        'descricao': 'Aplicação Java para simulação de um mundo com países e cidades. Carregamento de dados em CSV, análise estatística e filtragem.',
        'conceitos_aplicados': 'Parsing CSV, Arrays, ArrayList, HashMap, encapsulamento, JUnit testing, Checkstyle',
        'sigla_uc': '898',  # LP2
        'tecnologias': ['Java'],
        'repositorio_git': 'https://github.com/pedropiedade/deisiworld',
        'url_deploy': '',
    },
    {
        'nome': 'Aplicação de Desenvolvimento de Interfaces',
        'descricao': 'Projeto prático de desenvolvimento de interfaces web responsivas, com foco em usabilidade e design centrado no utilizador.',
        'conceitos_aplicados': 'HTML semântico, CSS Grid, Flexbox, media queries, acessibilidade, UX',
        'sigla_uc': '26141',  # Desenvolvimento de Interfaces Web
        'tecnologias': ['HTML5', 'CSS3', 'JavaScript'],
        'repositorio_git': 'https://github.com/pedropiedade/interfaces-web',
        'url_deploy': '',
    },
]

for p in projetos_data:
    uc = get_uc(p['sigla_uc'])
    if not uc:
        print(f"  ⚠ UC com sigla {p['sigla_uc']} não encontrada. A saltar projeto '{p['nome']}'.")
        continue

    projeto, created = Projeto.objects.get_or_create(
        nome=p['nome'],
        defaults={
            'descricao': p['descricao'],
            'conceitos_aplicados': p['conceitos_aplicados'],
            'unidade_curricular': uc,
            'repositorio_git': p.get('repositorio_git', ''),
            'url_deploy': p.get('url_deploy', ''),
        }
    )
    for tech_nome in p['tecnologias']:
        if tech_nome in tecnologias_obj:
            projeto.tecnologias.add(tecnologias_obj[tech_nome])
    print(f"  ✓ {projeto.nome} (UC: {uc.nome})")

# =========================================================
# COMPETÊNCIAS
# =========================================================
print("\n=== A importar Competências ===")

competencias_data = [
    # Hard Skills
    ('Desenvolvimento Web', 'Hard Skill', 'Capacidade de criar aplicações web full-stack usando Django, HTML, CSS e JavaScript.', 3),
    ('Programação Orientada a Objetos', 'Hard Skill', 'Domínio de conceitos como herança, polimorfismo, encapsulamento em Java e Python.', 3),
    ('Gestão de Bases de Dados', 'Hard Skill', 'Modelação relacional, escrita de queries SQL e utilização de ORMs como o Django ORM.', 3),
    ('Controlo de Versões com Git', 'Hard Skill', 'Uso diário de Git para gestão de código, branches e colaboração em equipa.', 4),
    ('Sistemas Operativos Linux', 'Hard Skill', 'Comandos shell, gestão de processos, sistema de ficheiros e scripting bash básico.', 2),
    ('Algoritmos e Estruturas de Dados', 'Hard Skill', 'Implementação e análise de algoritmos de ordenação, pesquisa e estruturas como árvores e grafos.', 2),
    # Soft Skills
    ('Trabalho em Equipa', 'Soft Skill', 'Experiência em projetos colaborativos académicos, usando Git e metodologias ágeis simples.', 4),
    ('Resolução de Problemas', 'Soft Skill', 'Abordagem sistemática a problemas técnicos, com capacidade de depuração e investigação independente.', 4),
    ('Comunicação Técnica', 'Soft Skill', 'Capacidade de documentar código, escrever relatórios técnicos e apresentar projetos.', 3),
    ('Aprendizagem Contínua', 'Soft Skill', 'Motivação para explorara novas tecnologias e manter-se atualizado na área de computação.', 5),
    ('Gestão do Tempo', 'Soft Skill', 'Capacidade de gerir múltiplos projetos académicos em simultâneo com prazos definidos.', 3),
]

for titulo, categoria, descricao, nivel in competencias_data:
    obj, _ = Competencia.objects.get_or_create(
        titulo=titulo,
        defaults={'categoria': categoria, 'descricao': descricao, 'nivel': nivel}
    )
    print(f"  ✓ {obj.titulo} ({obj.categoria})")

# =========================================================
# FORMAÇÕES
# =========================================================
print("\n=== A importar Formações ===")

formacoes_data = [
    {
        'titulo': 'Licenciatura em Engenharia Informática',
        'instituicao': 'Universidade Lusófona de Humanidades e Tecnologias',
        'data_inicio': date(2022, 9, 1),
        'data_fim': None,
        'descricao': 'Curso de 3 anos focado em desenvolvimento de software, sistemas de informação, redes e inteligência artificial.',
        'local': 'Lisboa, Portugal',
    },
    {
        'titulo': 'CS50: Introduction to Computer Science',
        'instituicao': 'Harvard University (edX)',
        'data_inicio': date(2023, 6, 1),
        'data_fim': date(2023, 8, 31),
        'descricao': 'Curso introdutório de ciência da computação da Harvard, cobrindo C, Python, SQL, HTML/CSS e Flask.',
        'local': 'Online',
    },
    {
        'titulo': 'Python para Ciência de Dados',
        'instituicao': 'Coursera / IBM',
        'data_inicio': date(2024, 1, 1),
        'data_fim': date(2024, 3, 31),
        'descricao': 'Curso de análise de dados com Python, Pandas, NumPy e Matplotlib. Incluiu projetos práticos com datasets reais.',
        'local': 'Online',
    },
    {
        'titulo': 'Git e GitHub para Iniciantes',
        'instituicao': 'Udemy',
        'data_inicio': date(2022, 10, 1),
        'data_fim': date(2022, 10, 31),
        'descricao': 'Formação prática em controlo de versões com Git e GitHub: commits, branches, merges e pull requests.',
        'local': 'Online',
    },
]

for f in formacoes_data:
    obj, _ = Formacao.objects.get_or_create(
        titulo=f['titulo'],
        defaults=f
    )
    print(f"  ✓ {obj.titulo}")

# =========================================================
# INTERESSES
# =========================================================
print("\n=== A importar Interesses ===")

interesses_data = [
    {
        'titulo': 'Inteligência Artificial e Machine Learning',
        'descricao': 'Fascinado pelo potencial da IA para resolver problemas reais. Interesse particular em NLP e modelos generativos.',
    },
    {
        'titulo': 'Desenvolvimento Web Full-Stack',
        'descricao': 'Apaixonado por criar aplicações web completas, desde o backend até ao design de interfaces intuitivas.',
    },
    {
        'titulo': 'Open Source',
        'descricao': 'Crença na filosofia open-source e interesse em contribuir para projetos da comunidade.',
    },
    {
        'titulo': 'Cibersegurança',
        'descricao': 'Curiosidade crescente sobre proteção de sistemas, criptografia e ethical hacking introdutório.',
    },
    {
        'titulo': 'Ciência de Dados',
        'descricao': 'Interesse em extrair conhecimento de dados através de visualização, estatística e machine learning.',
    },
    {
        'titulo': 'Desporto e Bem-estar',
        'descricao': 'A prática regular de desporto é fundamental para manter equilíbrio mental e física durante o percurso académico.',
    },
]

for i in interesses_data:
    obj, _ = Interesse.objects.get_or_create(titulo=i['titulo'], defaults=i)
    print(f"  ✓ {obj.titulo}")

# =========================================================
# RESUMO FINAL
# =========================================================
print("\n=== Importação concluída! ===")
print(f"  Tecnologias: {Tecnologia.objects.count()}")
print(f"  Projetos:    {Projeto.objects.count()}")
print(f"  Competências:{Competencia.objects.count()}")
print(f"  Formações:   {Formacao.objects.count()}")
print(f"  Interesses:  {Interesse.objects.count()}")
print(f"  TFCs:        {TFC.objects.count()}")
