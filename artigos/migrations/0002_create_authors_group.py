from django.db import migrations


GROUP_NAME = 'autores'
ARTIGOS_MODELS = [
    'artigo',
]


def create_authors_group(apps, schema_editor):
    ContentType = apps.get_model('contenttypes', 'ContentType')
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    group, _ = Group.objects.get_or_create(name=GROUP_NAME)
    permissions = []
    labels = {
        'add': 'Can add artigo',
        'change': 'Can change artigo',
        'view': 'Can view artigo',
    }

    for model_name in ARTIGOS_MODELS:
        content_type, _ = ContentType.objects.get_or_create(
            app_label='artigos',
            model=model_name,
        )
        for action, name in labels.items():
            permission, _ = Permission.objects.get_or_create(
                content_type=content_type,
                codename=f'{action}_{model_name}',
                defaults={'name': name},
            )
            permissions.append(permission)

    group.permissions.set(permissions)


class Migration(migrations.Migration):
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('artigos', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_authors_group, migrations.RunPython.noop),
    ]
