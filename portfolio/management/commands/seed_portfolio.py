import json
import os
from datetime import date
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from portfolio.models import (
    Competencia,
    Formacao,
    Interesse,
    Licenciatura,
    MakingOf,
    Projeto,
    Tecnologia,
    TFC,
    UnidadeCurricular,
)


class Command(BaseCommand):
    help = 'Carrega os dados essenciais do portfólio para uma base de dados vazia.'

    def handle(self, *args, **options):
        self.seed_course_data()
        self.seed_tfcs()
        self.seed_personal_data()
        self.seed_making_of()

        self.stdout.write(self.style.SUCCESS('Seed do portfólio concluído com sucesso.'))

    @property
    def base_dir(self):
        return Path(settings.BASE_DIR)

    def load_json(self, relative_path):
        file_path = self.base_dir / relative_path
        if not file_path.exists():
            self.stdout.write(self.style.WARNING(f'Ficheiro não encontrado: {relative_path}'))
            return None
        with file_path.open('r', encoding='utf-8') as file_handle:
            return json.load(file_handle)

    def seed_course_data(self):
        course_data = self.load_json('files/ULHT260-PT.json')
        if not course_data:
            return

        course_detail = course_data.get('courseDetail') or {}
        if not isinstance(course_detail, dict):
            course_detail = {}

        licenciatura, _ = Licenciatura.objects.update_or_create(
            nome=course_detail.get('courseName', 'Engenharia Informática'),
            defaults={
                'apresentacao': course_detail.get(
                    'presentation',
                    'Curso de Engenharia Informática da Universidade Lusófona.',
                ),
                'objetivos': course_detail.get(
                    'objectives',
                    'Formar profissionais qualificados na área de TI.',
                ),
                'competencias': course_detail.get(
                    'competences',
                    'Desenvolvimento de software, redes, sistemas e web.',
                ),
                'saidas_profissionais': course_detail.get(
                    'careerOportunities',
                    'Software Engineer, Systems Admin, Web Developer e áreas relacionadas.',
                ),
                'razoes_escolha': '\n'.join(
                    reason.get('reason', '') for reason in course_data.get('reasons', [])
                ),
            },
        )

        for uc_data in course_data.get('courseFlatPlan', []):
            uc_code = uc_data.get('curricularIUnitReadableCode', '')
            detail_data = self.load_json(f'files/{uc_code}-PT.json') or {}

            UnidadeCurricular.objects.update_or_create(
                sigla=uc_code.split('-')[-1],
                licenciatura=licenciatura,
                defaults={
                    'nome': uc_data.get('curricularUnitName', ''),
                    'ano': uc_data.get('curricularYear', 1),
                    'semestre': 1 if uc_data.get('semesterCode') == 'S' else 2,
                    'creditos': uc_data.get('ects', 0),
                    'objetivos': detail_data.get('objectives', ''),
                    'conteudos': detail_data.get('programme', ''),
                    'metodologia': detail_data.get('methodology', ''),
                    'bibliografia': detail_data.get('bibliography', ''),
                    'natureza': detail_data.get('nature', ''),
                    'avaliacao': detail_data.get('avaliacao', ''),
                },
            )

    def seed_tfcs(self):
        tfc_list = self.load_json('data/tfc_2025.json')
        if not tfc_list:
            return

        for tfc_data in tfc_list:
            TFC.objects.update_or_create(
                titulo=tfc_data['titulo'],
                defaults={
                    'autores': tfc_data['autores'],
                    'orientadores': tfc_data['orientadores'],
                    'ano': tfc_data['ano'],
                    'resumo': tfc_data['resumo'],
                    'destaque': tfc_data['destaque'],
                },
            )

    def seed_personal_data(self):
        public_url = os.getenv('APP_PUBLIC_URL', '')

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
                'descricao': 'Linguagem de estilos para definição visual de páginas web.',
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
                'descricao': 'Linguagem orientada a objetos amplamente utilizada em desenvolvimento empresarial e mobile.',
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
                'descricao': 'Linguagem de consulta para bases de dados relacionais.',
                'nivel_interesse': 4,
            },
            {
                'nome': 'Git',
                'link_oficial': 'https://git-scm.com',
                'descricao': 'Sistema de controlo de versões distribuído.',
                'nivel_interesse': 5,
            },
            {
                'nome': 'Linux',
                'link_oficial': 'https://www.linux.org',
                'descricao': 'Sistema operativo open-source usado em desenvolvimento e backend.',
                'nivel_interesse': 3,
            },
        ]

        tecnologias = {}
        for tecnologia in tecnologias_data:
            nome = tecnologia['nome']
            tecnologias[nome], _ = Tecnologia.objects.update_or_create(
                nome=nome,
                defaults={
                    'link_oficial': tecnologia['link_oficial'],
                    'descricao': tecnologia['descricao'],
                    'nivel_interesse': tecnologia['nivel_interesse'],
                },
            )

        projetos_data = [
            {
                'nome': 'Portfólio Web Pessoal',
                'descricao': 'Aplicação web desenvolvida em Django para apresentação do percurso académico e projetos.',
                'conceitos_aplicados': 'Framework Django, ORM, templates, admin, migrações, HTML/CSS e media files.',
                'sigla_uc': '11195',
                'tecnologias': ['Python', 'Django', 'HTML5', 'CSS3', 'SQL / SQLite'],
                'repositorio_git': 'https://github.com/PedroP0202/Projecto_Programacao_web_.git',
                'url_deploy': public_url,
            },
            {
                'nome': 'Sistema de Gestão de Biblioteca',
                'descricao': 'Aplicação de gestão de livros, autores e empréstimos com interface web básica em Django.',
                'conceitos_aplicados': 'Modelação relacional, ForeignKey, ManyToMany, Django ORM e SQL.',
                'sigla_uc': '1792',
                'tecnologias': ['Python', 'Django', 'SQL / SQLite'],
                'repositorio_git': 'https://github.com/pedropiedade/biblioteca-django',
                'url_deploy': '',
            },
            {
                'nome': 'Jogo da Forca em Java',
                'descricao': 'Jogo da forca em modo texto implementado em Java com programação orientada a objetos.',
                'conceitos_aplicados': 'POO, herança, polimorfismo, encapsulamento, ArrayList e exceções.',
                'sigla_uc': '898',
                'tecnologias': ['Java'],
                'repositorio_git': 'https://github.com/pedropiedade/jogo-forca-java',
                'url_deploy': '',
            },
            {
                'nome': 'Simulador de Mundo - DeisiWorld',
                'descricao': 'Aplicação Java para simulação de um mundo com países e cidades.',
                'conceitos_aplicados': 'Parsing CSV, Arrays, ArrayList, HashMap, encapsulamento e testes.',
                'sigla_uc': '898',
                'tecnologias': ['Java'],
                'repositorio_git': 'https://github.com/pedropiedade/deisiworld',
                'url_deploy': '',
            },
            {
                'nome': 'Aplicação de Desenvolvimento de Interfaces',
                'descricao': 'Projeto prático de interfaces web responsivas com foco em usabilidade.',
                'conceitos_aplicados': 'HTML semântico, CSS Grid, Flexbox, media queries, acessibilidade e UX.',
                'sigla_uc': '26141',
                'tecnologias': ['HTML5', 'CSS3', 'JavaScript'],
                'repositorio_git': 'https://github.com/pedropiedade/interfaces-web',
                'url_deploy': '',
            },
        ]

        for projeto_data in projetos_data:
            unidade_curricular = UnidadeCurricular.objects.filter(sigla=projeto_data['sigla_uc']).first()
            if not unidade_curricular:
                self.stdout.write(
                    self.style.WARNING(
                        f"Projeto ignorado por falta da UC {projeto_data['sigla_uc']}: {projeto_data['nome']}"
                    )
                )
                continue

            projeto, _ = Projeto.objects.update_or_create(
                nome=projeto_data['nome'],
                defaults={
                    'descricao': projeto_data['descricao'],
                    'conceitos_aplicados': projeto_data['conceitos_aplicados'],
                    'unidade_curricular': unidade_curricular,
                    'repositorio_git': projeto_data['repositorio_git'],
                    'url_deploy': projeto_data['url_deploy'],
                },
            )
            projeto.tecnologias.set(
                [tecnologias[nome] for nome in projeto_data['tecnologias'] if nome in tecnologias]
            )

        competencias_data = [
            ('Desenvolvimento Web', 'Hard Skill', 'Capacidade de criar aplicações web full-stack usando Django, HTML, CSS e JavaScript.', 3),
            ('Programação Orientada a Objetos', 'Hard Skill', 'Domínio de conceitos como herança, polimorfismo e encapsulamento em Java e Python.', 3),
            ('Gestão de Bases de Dados', 'Hard Skill', 'Modelação relacional, escrita de queries SQL e utilização de ORMs como o Django ORM.', 3),
            ('Controlo de Versões com Git', 'Hard Skill', 'Uso diário de Git para gestão de código e colaboração em equipa.', 4),
            ('Sistemas Operativos Linux', 'Hard Skill', 'Comandos shell, gestão de processos e scripting bash básico.', 2),
            ('Algoritmos e Estruturas de Dados', 'Hard Skill', 'Implementação e análise de algoritmos de ordenação, pesquisa e estruturas de dados.', 2),
            ('Trabalho em Equipa', 'Soft Skill', 'Experiência em projetos colaborativos académicos com Git e metodologias simples.', 4),
            ('Resolução de Problemas', 'Soft Skill', 'Abordagem sistemática a problemas técnicos, com capacidade de depuração.', 4),
            ('Comunicação Técnica', 'Soft Skill', 'Capacidade de documentar código e apresentar projetos.', 3),
            ('Aprendizagem Contínua', 'Soft Skill', 'Motivação para explorar novas tecnologias e manter-se atualizado.', 5),
            ('Gestão do Tempo', 'Soft Skill', 'Capacidade de gerir múltiplos projetos com prazos definidos.', 3),
        ]

        for titulo, categoria, descricao, nivel in competencias_data:
            Competencia.objects.update_or_create(
                titulo=titulo,
                defaults={
                    'categoria': categoria,
                    'descricao': descricao,
                    'nivel': nivel,
                },
            )

        formacoes_data = [
            {
                'titulo': 'Licenciatura em Engenharia Informática',
                'instituicao': 'Universidade Lusófona de Humanidades e Tecnologias',
                'data_inicio': date(2022, 9, 1),
                'data_fim': None,
                'descricao': 'Curso focado em desenvolvimento de software, sistemas de informação, redes e inteligência artificial.',
                'local': 'Lisboa, Portugal',
            },
            {
                'titulo': 'CS50: Introduction to Computer Science',
                'instituicao': 'Harvard University (edX)',
                'data_inicio': date(2023, 6, 1),
                'data_fim': date(2023, 8, 31),
                'descricao': 'Curso introdutório de ciência da computação cobrindo C, Python, SQL, HTML/CSS e Flask.',
                'local': 'Online',
            },
            {
                'titulo': 'Python para Ciência de Dados',
                'instituicao': 'Coursera / IBM',
                'data_inicio': date(2024, 1, 1),
                'data_fim': date(2024, 3, 31),
                'descricao': 'Curso de análise de dados com Python, Pandas, NumPy e Matplotlib.',
                'local': 'Online',
            },
            {
                'titulo': 'Git e GitHub para Iniciantes',
                'instituicao': 'Udemy',
                'data_inicio': date(2022, 10, 1),
                'data_fim': date(2022, 10, 31),
                'descricao': 'Formação prática em controlo de versões com Git e GitHub.',
                'local': 'Online',
            },
        ]

        for formacao in formacoes_data:
            Formacao.objects.update_or_create(
                titulo=formacao['titulo'],
                defaults=formacao,
            )

        interesses_data = [
            {
                'titulo': 'Inteligência Artificial e Machine Learning',
                'descricao': 'Interesse pelo potencial da IA para resolver problemas reais, com foco especial em NLP e modelos generativos.',
            },
            {
                'titulo': 'Desenvolvimento Web Full-Stack',
                'descricao': 'Gosto por criar aplicações web completas, desde o backend até à interface.',
            },
            {
                'titulo': 'Open Source',
                'descricao': 'Interesse em contribuir para projetos da comunidade e aprender com código aberto.',
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
                'descricao': 'A prática regular de desporto ajuda a manter equilíbrio durante o percurso académico.',
            },
        ]

        for interesse in interesses_data:
            Interesse.objects.update_or_create(
                titulo=interesse['titulo'],
                defaults={'descricao': interesse['descricao']},
            )

    def seed_making_of(self):
        MakingOf.objects.update_or_create(
            titulo='Decisões de Modelação e Importação de Dados',
            defaults={
                'descricao': 'Documentação das decisões tomadas durante a modelação e importação dos dados do portfólio.',
                'decisoes_tomadas': (
                    '1. Modelos académicos e pessoais mantidos separados para facilitar navegação e administração.\n'
                    '2. Dados das UCs e TFCs preparados para seed automático no deploy.\n'
                    '3. Deploy configurado para usar Postgres em produção em vez de SQLite.'
                ),
                'erros_e_correcoes': (
                    '- Ajuste da configuração para produção com ALLOWED_HOSTS e SECRET_KEY por ambiente.\n'
                    '- Remoção da dependência da base de dados local para deploy.\n'
                    '- Campo de imagem do Making Of tornado opcional para não bloquear o admin.'
                ),
                'uso_ia': 'A IA foi utilizada para acelerar a preparação do deploy, refatorar configurações e consolidar a seed de dados.',
            },
        )
