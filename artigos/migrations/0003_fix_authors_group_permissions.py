from django.db import migrations


GROUP_NAME = 'autores'


def fix_authors_group_permissions(apps, schema_editor):
    ContentType = apps.get_model('contenttypes', 'ContentType')
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    group, _ = Group.objects.get_or_create(name=GROUP_NAME)
    content_type, _ = ContentType.objects.get_or_create(
        app_label='artigos',
        model='artigo',
    )
    permissions = []
    for action, name in {
        'add': 'Can add artigo',
        'change': 'Can change artigo',
        'view': 'Can view artigo',
    }.items():
        permission, _ = Permission.objects.get_or_create(
            content_type=content_type,
            codename=f'{action}_artigo',
            defaults={'name': name},
        )
        permissions.append(permission)

    group.permissions.set(permissions)


class Migration(migrations.Migration):
    dependencies = [
        ('artigos', '0002_create_authors_group'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.RunPython(fix_authors_group_permissions, migrations.RunPython.noop),
    ]
