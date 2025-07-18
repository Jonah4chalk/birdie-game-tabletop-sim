# Generated by Django 5.2.1 on 2025-06-05 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aviary', '0024_alter_birdcard_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='draw_cards_cubes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='board',
            name='gain_food_cubes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='board',
            name='lay_eggs_cubes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='board',
            name='play_a_bird_cubes',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
