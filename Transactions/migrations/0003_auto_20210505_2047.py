# Generated by Django 2.2.10 on 2021-05-05 19:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Transactions', '0002_auto_20210505_0141'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='category_pred',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='etat',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='is_fraud_pred',
        ),
    ]
