# Generated by Django 4.1.5 on 2023-09-19 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aviary', '0006_habitats_birdcard_habitats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='birdcard',
            name='image',
            field=models.ImageField(upload_to='bird_images/'),
        ),
    ]