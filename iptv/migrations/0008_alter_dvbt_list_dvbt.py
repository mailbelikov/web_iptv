# Generated by Django 5.1.2 on 2025-01-30 10:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iptv', '0007_dvbt_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dvbt_list',
            name='dvbt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='dvbt_ch', to='iptv.dvbt'),
        ),
    ]
