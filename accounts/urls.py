from django.urls import path

from . import views


app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registo/', views.register_view, name='register'),
    path('magic-login/<uuid:token>/', views.magic_login_view, name='magic_login'),
]
