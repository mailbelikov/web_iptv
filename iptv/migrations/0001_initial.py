# Generated by Django 5.1.2 on 2025-01-27 10:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dvbt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('freq', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Dvbt_Channels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('sid', models.CharField(max_length=5)),
                ('udp_ip', models.CharField(blank=True, max_length=15)),
                ('udp_port', models.CharField(blank=True, max_length=5)),
                ('dvbt', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='iptv.dvbt')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
