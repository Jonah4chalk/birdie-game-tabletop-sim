# Generated by Django 4.1.5 on 2023-09-21 07:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aviary', '0012_rename_card_id_foodjunction_card_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='forest_1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Forest1', to='aviary.birdcard'),
        ),
        migrations.AlterField(
            model_name='board',
            name='forest_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Forest2', to='aviary.birdcard'),
        ),
        migrations.AlterField(
            model_name='board',
            name='forest_3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Forest3', to='aviary.birdcard'),
        ),
        migrations.AlterField(
            model_name='board',
            name='forest_4',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Forest4', to='aviary.birdcard'),
        ),
        migrations.AlterField(
            model_name='board',
            name='forest_5',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Forest5', to='aviary.birdcard'),
        ),
        migrations.AlterField(
            model_name='board',
            name='grassland_1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Grassland1', to='aviary.birdcard'),
        ),
        migrations.AlterField(
            model_name='board',
            name='grassland_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Grassland2', to='aviary.birdcard'),
        ),
        migrations.AlterField(
            model_name='board',
            name='grassland_3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Grassland3', to='aviary.birdcard'),
        ),
        migrations.AlterField(
            model_name='board',
            name='grassland_4',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Grassland4', to='aviary.birdcard'),
        ),
        migrations.AlterField(
            model_name='board',
            name='grassland_5',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Grassland5', to='aviary.birdcard'),
        ),
        migrations.AlterField(
            model_name='board',
            name='wetland_1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Wetland1', to='aviary.birdcard'),
        ),
        migrations.AlterField(
            model_name='board',
            name='wetland_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Wetland2', to='aviary.birdcard'),
        ),
        migrations.AlterField(
            model_name='board',
            name='wetland_3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Wetland3', to='aviary.birdcard'),
        ),
        migrations.AlterField(
            model_name='board',
            name='wetland_4',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Wetland4', to='aviary.birdcard'),
        ),
        migrations.AlterField(
            model_name='board',
            name='wetland_5',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Wetland5', to='aviary.birdcard'),
        ),
    ]
