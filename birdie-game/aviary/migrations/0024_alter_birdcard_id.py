# Generated by Django 5.2.1 on 2025-05-19 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aviary', '0023_board_bonus_cards_alter_endroundgoal_goal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='birdcard',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
