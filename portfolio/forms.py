from django import forms

from .models import (
    Competencia,
    Docente,
    Formacao,
    Interesse,
    Licenciatura,
    MakingOf,
    Projeto,
    Tecnologia,
    TFC,
    UnidadeCurricular,
)


class BasePortfolioModelForm(forms.ModelForm):
    required_css_class = 'required'


class LicenciaturaForm(BasePortfolioModelForm):
    class Meta:
        model = Licenciatura
        fields = '__all__'


class DocenteForm(BasePortfolioModelForm):
    class Meta:
        model = Docente
        fields = '__all__'


class UnidadeCurricularForm(BasePortfolioModelForm):
    class Meta:
        model = UnidadeCurricular
        fields = '__all__'


class ProjetoForm(BasePortfolioModelForm):
    class Meta:
        model = Projeto
        fields = '__all__'


class TecnologiaForm(BasePortfolioModelForm):
    class Meta:
        model = Tecnologia
        fields = '__all__'


class CompetenciaForm(BasePortfolioModelForm):
    class Meta:
        model = Competencia
        fields = '__all__'


class InteresseForm(BasePortfolioModelForm):
    class Meta:
        model = Interesse
        fields = '__all__'


class FormacaoForm(BasePortfolioModelForm):
    class Meta:
        model = Formacao
        fields = '__all__'


class TFCForm(BasePortfolioModelForm):
    class Meta:
        model = TFC
        fields = '__all__'


class MakingOfForm(BasePortfolioModelForm):
    class Meta:
        model = MakingOf
        fields = [
            'titulo',
            'descricao',
            'imagem_caderno',
            'decisoes_tomadas',
            'erros_e_correcoes',
            'uso_ia',
        ]
