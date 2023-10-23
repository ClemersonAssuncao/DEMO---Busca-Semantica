# Generated by Django 4.2 on 2023-10-21 14:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('material', '0006_alter_file_dt_updated_alter_file_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='dt_created',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Data de criação'),
        ),
        migrations.AlterField(
            model_name='file',
            name='user_created',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='usuario_criacao', to=settings.AUTH_USER_MODEL, verbose_name='Criado por: '),
        ),
    ]
