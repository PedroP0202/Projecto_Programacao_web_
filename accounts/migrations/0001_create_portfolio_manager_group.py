from django.db import migrations


GROUP_NAME = 'gestor-portfolio'
PORTFOLIO_MODELS = [
    'competencia',
    'docente',
    'formacao',
    'interesse',
    'licenciatura',
    'makingof',
    'projeto',
    'tecnologia',
    'tfc',
    'unidadecurricular',
]


def create_portfolio_manager_group(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    group, _ = Group.objects.get_or_create(name=GROUP_NAME)
    codenames = [
        f'{action}_{model_name}'
        for model_name in PORTFOLIO_MODELS
        for action in ['add', 'change', 'delete', 'view']
    ]
    permissions = Permission.objects.filter(
        content_type__app_label='portfolio',
        content_type__model__in=PORTFOLIO_MODELS,
        codename__in=codenames,
    )
    group.permissions.set(permissions)


class Migration(migrations.Migration):
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('portfolio', '0005_alter_makingof_imagem_caderno'),
    ]

    operations = [
        migrations.RunPython(create_portfolio_manager_group, migrations.RunPython.noop),
    ]
