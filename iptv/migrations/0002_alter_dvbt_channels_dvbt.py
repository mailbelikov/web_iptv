# Generated by Django 5.1.2 on 2025-01-29 04:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iptv', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dvbt_channels',
            name='dvbt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='channels', to='iptv.dvbt'),
        ),
    ]
