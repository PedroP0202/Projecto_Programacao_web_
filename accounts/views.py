from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import MagicLinkRequestForm, RegisterForm
from .models import MagicLoginToken


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    magic_form = MagicLinkRequestForm()

    if request.method == 'POST':
        if request.POST.get('auth_method') == 'magic_link':
            magic_form = MagicLinkRequestForm(request.POST)
            if magic_form.is_valid():
                send_magic_link(request, magic_form.cleaned_data['email'])
                messages.success(
                    request,
                    'Se existir uma conta com esse email, receberá um link mágico para entrar.',
                )
                return redirect('accounts:login')
        else:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect(request.GET.get('next') or 'home')

            messages.error(request, 'Nome de utilizador ou password inválidos.')

    return render(request, 'accounts/login.html', {'magic_form': magic_form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Sessão terminada com sucesso.')
    return redirect('home')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            autores_group, _ = Group.objects.get_or_create(name='autores')
            user.groups.add(autores_group)
            login(request, user)
            messages.success(request, 'Registo efetuado com sucesso.')
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def magic_login_view(request, token):
    magic_token = get_object_or_404(MagicLoginToken, token=token)

    if not magic_token.is_valid():
        messages.error(request, 'O link mágico é inválido, expirou ou já foi usado.')
        return redirect('accounts:login')

    user = magic_token.user
    magic_token.mark_as_used()
    login(request, user)
    messages.success(request, 'Sessão iniciada com link mágico.')

    if magic_token.redirect_path:
        return redirect(magic_token.redirect_path)
    return redirect('home')


def send_magic_link(request, email):
    user = User.objects.filter(email__iexact=email, is_active=True).first()
    if user is None:
        return

    redirect_path = get_safe_next_url(request)
    magic_token = MagicLoginToken.objects.create(
        user=user,
        redirect_path=redirect_path,
    )
    magic_url = request.build_absolute_uri(
        reverse('accounts:magic_login', kwargs={'token': magic_token.token})
    )

    send_mail(
        subject='O seu link mágico de acesso',
        message=(
            'Use este link para entrar no portfólio:\n\n'
            f'{magic_url}\n\n'
            'Este link expira em 15 minutos e só pode ser usado uma vez.'
        ),
        from_email=None,
        recipient_list=[user.email],
        fail_silently=False,
    )


def get_safe_next_url(request):
    next_url = request.GET.get('next', '')
    if url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return next_url
    return ''
