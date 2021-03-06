# Generated by Django 3.0.6 on 2020-07-02 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalog', '0002_catalog_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prize',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('description', models.CharField(max_length=60)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('catalog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Catalog')),
            ],
        ),
    ]
