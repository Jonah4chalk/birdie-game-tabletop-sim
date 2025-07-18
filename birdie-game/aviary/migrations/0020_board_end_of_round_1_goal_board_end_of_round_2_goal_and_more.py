# Generated by Django 5.2.1 on 2025-05-13 23:37

import aviary.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aviary', '0019_bonuscard_remove_board_end_of_round_1_goal_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='end_of_round_1_goal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='EndRoundGoal1', to='aviary.endroundgoal'),
        ),
        migrations.AddField(
            model_name='board',
            name='end_of_round_2_goal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='EndRoundGoal2', to='aviary.endroundgoal'),
        ),
        migrations.AddField(
            model_name='board',
            name='end_of_round_3_goal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='EndRoundGoal3', to='aviary.endroundgoal'),
        ),
        migrations.AddField(
            model_name='board',
            name='end_of_round_4_goal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='EndRoundGoal4', to='aviary.endroundgoal'),
        ),
    ]
