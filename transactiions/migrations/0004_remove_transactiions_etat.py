# Generated by Django 2.2.10 on 2021-05-15 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactiions', '0003_auto_20210508_0213'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactiions',
            name='etat',
        ),
    ]
