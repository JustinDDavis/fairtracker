# Generated by Django 3.0.6 on 2020-06-28 02:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('fair', '0002_fair_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('description', models.CharField(max_length=60)),
                ('fair', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fair.Fair')),
            ],
        ),
    ]
