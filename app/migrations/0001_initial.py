# Generated by Django 2.2.10 on 2021-05-04 13:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amt', models.FloatField(null=True)),
                ('category', models.CharField(max_length=100, null=True)),
                ('hours', models.IntegerField()),
                ('dob', models.DateField(null=True)),
                ('month', models.IntegerField()),
                ('gender', models.CharField(max_length=100, null=True)),
                ('unix_time', models.FloatField(null=True)),
                ('year', models.IntegerField()),
                ('day', models.IntegerField()),
                ('city_pop', models.CharField(max_length=100, null=True)),
                ('merchant', models.CharField(max_length=100)),
                ('is_fraud', models.IntegerField()),
                ('status', models.CharField(max_length=100, null=True)),
                ('category_pred', models.CharField(max_length=100, null=True)),
                ('is_fraud_pred', models.IntegerField()),
                ('etat', models.CharField(choices=[('En cours', 'En cours'), ('En traitement', 'En traitement'), ('Traitée', 'Traitée')], max_length=100, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
