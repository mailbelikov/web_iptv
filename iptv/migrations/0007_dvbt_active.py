# Generated by Django 5.1.2 on 2025-01-30 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iptv', '0006_delete_dvbt_channels'),
    ]

    operations = [
        migrations.AddField(
            model_name='dvbt',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
