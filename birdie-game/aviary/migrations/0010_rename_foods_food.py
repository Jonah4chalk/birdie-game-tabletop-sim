# Generated by Django 4.1.5 on 2023-09-19 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aviary', '0009_rename_habitats_habitat'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Foods',
            new_name='Food',
        ),
    ]
