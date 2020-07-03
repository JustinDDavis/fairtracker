# Generated by Django 3.0.6 on 2020-07-03 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('participant', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='city',
            field=models.CharField(default='NoCity', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='participant',
            name='static_participant_id',
            field=models.CharField(default=None, max_length=60, null=True),
        ),
    ]