from django.db import models

class Licenciatura(models.Model):
    nome = models.CharField(max_length=100)
    apresentacao = models.TextField()
    objetivos = models.TextField()
    competencias = models.TextField()
    saidas_profissionais = models.TextField()

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
    repositorio_git = models.URLField()

    def __str__(self):
        return self.nome
