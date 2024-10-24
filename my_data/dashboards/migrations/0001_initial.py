# Generated by Django 5.1.2 on 2024-10-21 00:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('charts', '0001_initial'),
        ('registration', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dashboard',
            fields=[
                ('dashboard_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('created_time', models.DateTimeField(auto_now=True)),
                ('charts', models.ManyToManyField(related_name='dashboards', to='charts.chart')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.user')),
            ],
            options={
                'verbose_name': 'Дашборд',
                'verbose_name_plural': 'Дашборды',
                'db_table': 'dashboards',
                'managed': True,
            },
        ),
    ]
