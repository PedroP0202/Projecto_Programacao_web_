import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Artigo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=160)),
                ('texto', models.TextField()),
                ('fotografia', models.ImageField(blank=True, null=True, upload_to='artigos/')),
                ('link_externo', models.URLField(blank=True, null=True, verbose_name='link externo')),
                ('data_criacao', models.DateTimeField(auto_now_add=True, verbose_name='data de criação')),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='artigos', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'artigo',
                'verbose_name_plural': 'artigos',
                'ordering': ['-data_criacao'],
            },
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField()),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('artigo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comentarios', to='artigos.artigo')),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comentarios_artigos', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'comentário',
                'verbose_name_plural': 'comentários',
                'ordering': ['data_criacao'],
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(blank=True, max_length=40, null=True)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('artigo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='artigos.artigo')),
                ('utilizador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='likes_artigos', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='like',
            constraint=models.UniqueConstraint(condition=models.Q(('utilizador__isnull', False)), fields=('artigo', 'utilizador'), name='unique_like_artigo_utilizador'),
        ),
        migrations.AddConstraint(
            model_name='like',
            constraint=models.UniqueConstraint(condition=models.Q(('session_key__isnull', False)), fields=('artigo', 'session_key'), name='unique_like_artigo_session'),
        ),
    ]
