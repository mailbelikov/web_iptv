# Generated by Django 5.1.5 on 2025-02-01 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iptv', '0014_streams_streams_list_delete_stream_streams_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streams',
            name='udp_ip',
            field=models.CharField(max_length=15, unique=True, verbose_name='IP адрес'),
        ),
    ]
