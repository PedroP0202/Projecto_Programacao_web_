from django.db import models

class Licenciatura(models.Model):
    nome = models.CharField(max_length=100)
    apresentacao = models.TextField()
    objetivos = models.TextField()
    competencias = models.TextField()
    saidas_profissionais = models.TextField()
    razoes_escolha = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nome

class Docente(models.Model):
    nome = models.CharField(max_length=100)
    link_lusofona = models.URLField()

    def __str__(self):
        return self.nome

class UnidadeCurricular(models.Model):
    nome = models.CharField(max_length=100)
    sigla = models.CharField(max_length=10)
    ano = models.IntegerField()
    semestre = models.IntegerField()
    creditos = models.IntegerField()
    licenciatura = models.ForeignKey(Licenciatura, on_delete=models.CASCADE, related_name='ucs')
    docentes = models.ManyToManyField(Docente, related_name='ucs')
    imagem = models.ImageField(upload_to='ucs/', null=True, blank=True)
    objetivos = models.TextField(null=True, blank=True)
    conteudos = models.TextField(null=True, blank=True)
    metodologia = models.TextField(null=True, blank=True)
    bibliografia = models.TextField(null=True, blank=True)
    natureza = models.CharField(max_length=50, null=True, blank=True)
    avaliacao = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.nome} ({self.sigla})"

class Tecnologia(models.Model):
    nome = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='tecnologias/', null=True, blank=True)
    link_oficial = models.URLField()
    descricao = models.TextField()
    nivel_interesse = models.IntegerField(default=1)

    def __str__(self):
        return self.nome

class Projeto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    conceitos_aplicados = models.TextField()
    tecnologias = models.ManyToManyField(Tecnologia, related_name='projetos')
    unidade_curricular = models.ForeignKey(UnidadeCurricular, on_delete=models.CASCADE, related_name='projetos')
    imagem = models.ImageField(upload_to='projetos/', null=True, blank=True)
    video_link = models.URLField(null=True, blank=True)
    repositorio_git = models.URLField(null=True, blank=True)
    url_deploy = models.URLField(null=True, blank=True)  # URL do projeto publicado

    def __str__(self):
        return self.nome

class TFC(models.Model):
    titulo = models.CharField(max_length=200)
    autores = models.CharField(max_length=200)
    orientadores = models.CharField(max_length=200)
    ano = models.IntegerField()
    resumo = models.TextField()
    link_repositorio = models.URLField(null=True, blank=True)  # Link para o repositório do TFC
    imagem = models.ImageField(upload_to='tfcs/', null=True, blank=True)
    destaque = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo

class Competencia(models.Model):
    NIVEL_CHOICES = [(1, 'Básico'), (2, 'Intermédio'), (3, 'Avançado'), (4, 'Especialista')]
    titulo = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50)  # ex: Soft Skill, Hard Skill
    descricao = models.TextField()
    nivel = models.IntegerField(choices=NIVEL_CHOICES, default=1)  # Nível de proficiência

    def __str__(self):
        return self.titulo

class Formacao(models.Model):
    titulo = models.CharField(max_length=100)
    instituicao = models.CharField(max_length=100)
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    descricao = models.TextField()
    local = models.CharField(max_length=100)

    def __str__(self):
        return self.titulo

class MakingOf(models.Model):
    data = models.DateTimeField(auto_now_add=True)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    imagem_caderno = models.ImageField(upload_to='makingof/')
    decisoes_tomadas = models.TextField()
    erros_e_correcoes = models.TextField()
    uso_ia = models.TextField()

    def __str__(self):
        return f"{self.titulo} - {self.data.strftime('%d/%m/%Y')}"

class Interesse(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='interesses/', null=True, blank=True)

    def __str__(self):
        return self.titulo
