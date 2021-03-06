# Generated by Django 3.0.6 on 2020-07-02 20:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('prize', '0001_initial'),
        ('participant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JudgeSheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participant_judge_sheet_set', to='participant.Participant')),
                ('prize', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prize_judge_sheet_set', to='prize.Prize')),
            ],
        ),
    ]
