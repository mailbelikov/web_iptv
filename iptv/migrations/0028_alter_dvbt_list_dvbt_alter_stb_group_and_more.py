# Generated by Django 5.1.2 on 2025-02-04 06:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iptv', '0027_alter_groups_options_alter_stb_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dvbt_list',
            name='dvbt',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='dvbt_ch', to='iptv.dvbt', verbose_name='Канал'),
        ),
        migrations.AlterField(
            model_name='stb',
            name='group',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='stb_list', to='iptv.groups', verbose_name='Группа'),
        ),
        migrations.AlterField(
            model_name='stb',
            name='stb_type',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='stb_list', to='iptv.stb_type', verbose_name='Тип'),
        ),
    ]
