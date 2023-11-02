# Generated by Django 4.2 on 2023-10-21 01:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('material', '0003_rename_directory_folder'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='PK')),
                ('name', models.CharField(max_length=255, verbose_name='Nome')),
                ('description', models.TextField(max_length=255, verbose_name='Descrição')),
                ('dt_created', models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')),
                ('dt_updated', models.DateTimeField(auto_now=True, verbose_name='Data de atualização')),
                ('id_folder', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='material.folder')),
                ('user_created', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuario_criacao', to=settings.AUTH_USER_MODEL, verbose_name='Criado por: ')),
                ('user_updated', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuario_atualizacao', to=settings.AUTH_USER_MODEL, verbose_name='Atualizado por: ')),
            ],
        ),
    ]