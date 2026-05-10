from django import forms

from .models import Artigo, Comentario


class ArtigoForm(forms.ModelForm):
    class Meta:
        model = Artigo
        fields = ['titulo', 'texto', 'fotografia', 'link_externo']


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        labels = {
            'texto': 'Comentário',
        }
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 3}),
        }
