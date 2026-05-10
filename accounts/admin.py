from django.contrib import admin

from .models import MagicLoginToken


@admin.register(MagicLoginToken)
class MagicLoginTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'token', 'created_at', 'used_at']
    search_fields = ['user__username', 'user__email', 'token']
    readonly_fields = ['token', 'created_at', 'used_at']
