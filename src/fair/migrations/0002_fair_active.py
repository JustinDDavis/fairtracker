# Generated by Django 3.0.6 on 2020-06-11 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fair', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fair',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
