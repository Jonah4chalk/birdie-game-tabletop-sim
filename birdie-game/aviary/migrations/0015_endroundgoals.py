# Generated by Django 4.1.5 on 2023-12-21 01:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aviary', '0014_birdcard_eggs'),
    ]

    operations = [
        migrations.CreateModel(
            name='EndRoundGoals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goal', models.CharField(max_length=200)),
                ('round', models.PositiveIntegerField(default=1)),
                ('board', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='aviary.board')),
            ],
        ),
    ]