from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Exists, OuterRef
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ArtigoForm, ComentarioForm
from .models import Artigo, Like
from .utils import user_is_author


author_required = user_passes_test(user_is_author)


def lista_artigos(request):
    liked_filter = get_liked_filter(request)
    artigos = list(
        Artigo.objects.select_related('autor')
        .prefetch_related('comentarios__autor')
        .annotate(likes_count=Count('likes', distinct=True))
        .annotate(user_liked=Exists(liked_filter.filter(artigo=OuterRef('pk'))))
    )
    for artigo in artigos:
        artigo.comentario_form = ComentarioForm(prefix=f'comentario-{artigo.pk}')

    return render(
        request,
        'artigos/lista.html',
        {
            'artigos': artigos,
        },
    )


@login_required
@author_required
def criar_artigo(request):
    if request.method == 'POST':
        form = ArtigoForm(request.POST, request.FILES)
        if form.is_valid():
            artigo = form.save(commit=False)
            artigo.autor = request.user
            artigo.save()
            messages.success(request, 'Artigo publicado com sucesso.')
            return redirect('artigos:lista')
    else:
        form = ArtigoForm()

    return render(
        request,
        'artigos/form.html',
        {
            'form': form,
            'title': 'Publicar artigo',
        },
    )


@login_required
@author_required
def editar_artigo(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk)
    if artigo.autor != request.user:
        raise PermissionDenied('Só pode editar os seus próprios artigos.')

    if request.method == 'POST':
        form = ArtigoForm(request.POST, request.FILES, instance=artigo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Artigo atualizado com sucesso.')
            return redirect('artigos:lista')
    else:
        form = ArtigoForm(instance=artigo)

    return render(
        request,
        'artigos/form.html',
        {
            'form': form,
            'title': 'Editar artigo',
        },
    )


@require_POST
def gostar_artigo(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk)
    like_kwargs = get_like_kwargs(request)
    like, created = Like.objects.get_or_create(artigo=artigo, **like_kwargs)

    if created:
        messages.success(request, 'Gostou deste artigo.')
    else:
        like.delete()
        messages.success(request, 'Like removido.')

    return redirect('artigos:lista')


@login_required
@require_POST
def comentar_artigo(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk)
    form = ComentarioForm(request.POST, prefix=f'comentario-{artigo.pk}')

    if form.is_valid():
        comentario = form.save(commit=False)
        comentario.artigo = artigo
        comentario.autor = request.user
        comentario.save()
        messages.success(request, 'Comentário publicado com sucesso.')
    else:
        messages.error(request, 'Não foi possível publicar o comentário.')

    return redirect('artigos:lista')


def get_like_kwargs(request):
    if request.user.is_authenticated:
        return {'utilizador': request.user}

    if not request.session.session_key:
        request.session.create()
    return {'session_key': request.session.session_key}


def get_liked_filter(request):
    if request.user.is_authenticated:
        return Like.objects.filter(utilizador=request.user)

    session_key = request.session.session_key
    if not session_key:
        return Like.objects.none()
    return Like.objects.filter(session_key=session_key)
