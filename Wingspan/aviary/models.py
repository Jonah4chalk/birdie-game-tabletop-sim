from django.db import models
from django.core.validators import MaxValueValidator
from django.utils.translation import gettext_lazy as _
# Create your models here.

class BirdCard(models.Model):
    # nest types
    NEST_TYPES = (
        ('g', 'Ground'),
        ('c', 'Cavity'),
        ('b', 'Bowl'),
        ('s', 'Stick'),
        ('n', 'None'),
        ('a', 'Star'),
    )

    # ability types
    ABILITY_TYPES = (
        ('w', 'White'),
        ('b', 'Brown'),
        ('t', 'Teal'),
        ('y', 'Yellow'),
        ('p', 'Pink'),
    )

    # direction facing
    FACING_DIRECTION = (
        ('r', 'Right'),
        ('l', 'Left'),
        ('f', 'Forward'),
    )

    name = models.CharField(max_length=50)
    image = models.ImageField()
    nest_size = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(6)])
    nest_type = models.CharField(max_length=1, choices=NEST_TYPES, default='n')
    wingspan = models.PositiveIntegerField(default=1)
    # habitats = models.ManyToManyField(Habitat)
    feathers = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(9)])
    ability_desc = models.CharField(max_length=200)
    ability_type = models.CharField(max_length=1, choices=ABILITY_TYPES, default='w')
    cached_food = models.PositiveIntegerField(default=0)
    tucked_cards = models.PositiveIntegerField(default=0)
    direction_facing = models.CharField(max_length=1, choices=FACING_DIRECTION, default='f')

    def __str__(self):
        return self.name
    
class Board(models.Model):
    forest_nectar = models.PositiveIntegerField(default=0)
    forest_1 = models.ForeignKey(BirdCard, related_name="Forest1", on_delete=models.SET_NULL, null=True)
    forest_2 = models.ForeignKey(BirdCard, related_name="Forest2", on_delete=models.SET_NULL, null=True)
    forest_3 = models.ForeignKey(BirdCard, related_name="Forest3", on_delete=models.SET_NULL, null=True)
    forest_4 = models.ForeignKey(BirdCard, related_name="Forest4", on_delete=models.SET_NULL, null=True)
    forest_5 = models.ForeignKey(BirdCard, related_name="Forest5", on_delete=models.SET_NULL, null=True)
    grassland_nectar = models.PositiveIntegerField(default=0)
    grassland_1 = models.ForeignKey(BirdCard, related_name="Grassland1", on_delete=models.SET_NULL, null=True)
    grassland_2 = models.ForeignKey(BirdCard, related_name="Grassland2", on_delete=models.SET_NULL, null=True)
    grassland_3 = models.ForeignKey(BirdCard, related_name="Grassland3", on_delete=models.SET_NULL, null=True)
    grassland_4 = models.ForeignKey(BirdCard, related_name="Grassland4", on_delete=models.SET_NULL, null=True)
    grassland_5 = models.ForeignKey(BirdCard, related_name="Grassland5", on_delete=models.SET_NULL, null=True)
    wetland_nectar = models.PositiveIntegerField(default=0)
    wetland_1 = models.ForeignKey(BirdCard, related_name="Wetland1", on_delete=models.SET_NULL, null=True)
    wetland_2 = models.ForeignKey(BirdCard, related_name="Wetland2", on_delete=models.SET_NULL, null=True)
    wetland_3 = models.ForeignKey(BirdCard, related_name="Wetland3", on_delete=models.SET_NULL, null=True)
    wetland_4 = models.ForeignKey(BirdCard, related_name="Wetland4", on_delete=models.SET_NULL, null=True)
    wetland_5 = models.ForeignKey(BirdCard, related_name="Wetland5", on_delete=models.SET_NULL, null=True)

class Foods(models.Model):
    id = models.AutoField(primary_key=True)
    food_name = models.CharField(max_length=6, default="default")

    def __str__(self):
        return self.food_name

class FoodJunction(models.Model):
    card_id = models.ForeignKey(BirdCard, on_delete=models.CASCADE)
    food_id = models.ForeignKey(Foods, on_delete=models.CASCADE)