# Generated by Django 5.1.2 on 2025-02-04 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iptv', '0026_stb_type_remote_control_stb'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='groups',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='stb',
            options={'ordering': ['ip_address', 'mac_address']},
        ),
        migrations.AlterModelOptions(
            name='stb_type',
            options={'ordering': ['model', 'name']},
        ),
        migrations.AlterField(
            model_name='stb_type',
            name='remote_control',
            field=models.CharField(max_length=15, verbose_name='Удаленный доступ'),
        ),
    ]
