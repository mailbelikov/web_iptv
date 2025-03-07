# Generated by Django 5.1.2 on 2025-01-31 07:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iptv', '0010_alter_dvbt_active_alter_dvbt_freq_alter_dvbt_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='streams_list',
            name='stream',
        ),
        migrations.AddField(
            model_name='streams',
            name='content',
            field=models.ManyToManyField(to='iptv.streams_list'),
        ),
        migrations.AlterField(
            model_name='dvbt',
            name='freq',
            field=models.CharField(blank=True, max_length=3, verbose_name='Частота'),
        ),
        migrations.AlterField(
            model_name='dvbt',
            name='name',
            field=models.CharField(blank=True, max_length=20, verbose_name='Канал'),
        ),
        migrations.AlterField(
            model_name='dvbt_list',
            name='dvbt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='dvbt_ch', to='iptv.dvbt', verbose_name='Канал'),
        ),
        migrations.AlterField(
            model_name='dvbt_list',
            name='name',
            field=models.CharField(blank=True, max_length=20, verbose_name='Программа'),
        ),
        migrations.AlterField(
            model_name='dvbt_list',
            name='sid',
            field=models.CharField(blank=True, max_length=5, verbose_name='SIG'),
        ),
        migrations.AlterField(
            model_name='dvbt_list',
            name='udp_ip',
            field=models.CharField(blank=True, max_length=15, verbose_name='IP адрес'),
        ),
        migrations.AlterField(
            model_name='dvbt_list',
            name='udp_port',
            field=models.CharField(blank=True, max_length=5, verbose_name='IP порт'),
        ),
        migrations.AlterField(
            model_name='streams',
            name='name',
            field=models.CharField(blank=True, max_length=40, verbose_name='Примечание'),
        ),
        migrations.AlterField(
            model_name='streams',
            name='type_content',
            field=models.CharField(blank=True, max_length=15, verbose_name='Тип контента'),
        ),
        migrations.AlterField(
            model_name='streams',
            name='udp_ip',
            field=models.CharField(default='224.224.224.1', max_length=15, primary_key=True, serialize=False, verbose_name='IP адрес'),
        ),
        migrations.AlterField(
            model_name='streams',
            name='udp_port',
            field=models.CharField(blank=True, max_length=5, verbose_name='IP порт'),
        ),
        migrations.AlterField(
            model_name='streams_list',
            name='name',
            field=models.CharField(blank=True, max_length=40, verbose_name='Примечание'),
        ),
        migrations.AlterField(
            model_name='streams_list',
            name='source',
            field=models.CharField(blank=True, max_length=254, verbose_name='Контент'),
        ),
    ]
