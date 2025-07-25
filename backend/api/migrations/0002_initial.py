# Generated by Django 5.2.4 on 2025-07-11 14:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='documentocliente',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documentos', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='documentoleido',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='documentoleido',
            name='documento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lecturas', to='api.documentocliente'),
        ),
        migrations.AddField(
            model_name='mensajecliente',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='documentoleido',
            unique_together={('documento', 'cliente')},
        ),
    ]
