# Generated by Django 4.1.5 on 2023-09-21 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aviary', '0010_rename_foods_food'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foodjunction',
            name='food_id',
        ),
        migrations.AddField(
            model_name='foodjunction',
            name='food_id',
            field=models.ManyToManyField(to='aviary.food'),
        ),
    ]
