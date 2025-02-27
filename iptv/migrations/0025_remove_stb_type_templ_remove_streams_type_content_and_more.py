# Generated by Django 5.1.2 on 2025-02-04 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iptv', '0024_alter_groups_start_stream'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stb_type',
            name='templ',
        ),
        migrations.RemoveField(
            model_name='streams',
            name='type_content',
        ),
        migrations.AddField(
            model_name='stb_type',
            name='home_page',
            field=models.CharField(blank=True, max_length=30, verbose_name='Домашняя страница'),
        ),
        migrations.AddField(
            model_name='stb_type',
            name='server_path',
            field=models.CharField(blank=True, max_length=30, verbose_name='Путь на сервере'),
        ),
        migrations.AddField(
            model_name='stb_type',
            name='template',
            field=models.CharField(blank=True, max_length=20, verbose_name='Шаблон'),
        ),
    ]
