# Generated by Django 5.2.1 on 2025-05-15 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aviary', '0021_alter_endroundgoal_goal'),
    ]

    operations = [
        migrations.AddField(
            model_name='bonuscard',
            name='score',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='endroundgoal',
            name='score',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
