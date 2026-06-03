from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ginasio_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercicio',
            name='descricao',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='planotreino',
            name='descricao',
            field=models.TextField(blank=True),
        ),
    ]
