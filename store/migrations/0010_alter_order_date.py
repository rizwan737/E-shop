# Generated by Django 3.2.8 on 2021-11-10 15:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_auto_20211110_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(default=datetime.datetime.today),
        ),
    ]
