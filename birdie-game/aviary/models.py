from django.db import models
from django.core.validators import MaxValueValidator
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Habitat(models.Model):
    id = models.AutoField(primary_key=True)
    habitat_name = models.CharField(max_length=9, default="forest")

    def __str__(self):
        return self.habitat_name

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
    nest_size = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(6)])
    nest_type = models.CharField(max_length=1, choices=NEST_TYPES, default='n')
    wingspan = models.PositiveIntegerField(default=1)
    habitats = models.ManyToManyField(Habitat)
    feathers = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(9)])
    ability_desc = models.CharField(max_length=200)
    ability_type = models.CharField(max_length=1, choices=ABILITY_TYPES, default='w')
    eggs = models.PositiveIntegerField(default=0)
    cached_food = models.PositiveIntegerField(default=0)
    tucked_cards = models.PositiveIntegerField(default=0)
    direction_facing = models.CharField(max_length=1, choices=FACING_DIRECTION, default='f')

    def __str__(self):
        return self.name
    
    def clean(self):
        if self.eggs > self.nest_size:
            raise ValidationError("This bird's nest cannot fit all of these eggs!")
        
    class Meta:
        ordering = ['name']

    
class EndRoundGoal(models.Model):
    goal = models.CharField(max_length=200)
    round = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.goal
    
    @classmethod
    def create_default_goal(cls):
        goal, created = cls.objects.get_or_create(
            goal="No Goal",
            round=1,
        )
        return goal.pk

    
class Board(models.Model):
    forest_nectar = models.PositiveIntegerField(default=0)
    forest_1 = models.ForeignKey("BirdCard", related_name="Forest1", on_delete=models.SET_NULL, null=True, blank=True)
    forest_2 = models.ForeignKey("BirdCard", related_name="Forest2", on_delete=models.SET_NULL, null=True, blank=True)
    forest_3 = models.ForeignKey("BirdCard", related_name="Forest3", on_delete=models.SET_NULL, null=True, blank=True)
    forest_4 = models.ForeignKey("BirdCard", related_name="Forest4", on_delete=models.SET_NULL, null=True, blank=True)
    forest_5 = models.ForeignKey("BirdCard", related_name="Forest5", on_delete=models.SET_NULL, null=True, blank=True)
    grassland_nectar = models.PositiveIntegerField(default=0)
    grassland_1 = models.ForeignKey("BirdCard", related_name="Grassland1", on_delete=models.SET_NULL, null=True, blank=True)
    grassland_2 = models.ForeignKey("BirdCard", related_name="Grassland2", on_delete=models.SET_NULL, null=True, blank=True)
    grassland_3 = models.ForeignKey("BirdCard", related_name="Grassland3", on_delete=models.SET_NULL, null=True, blank=True)
    grassland_4 = models.ForeignKey("BirdCard", related_name="Grassland4", on_delete=models.SET_NULL, null=True, blank=True)
    grassland_5 = models.ForeignKey("BirdCard", related_name="Grassland5", on_delete=models.SET_NULL, null=True, blank=True)
    wetland_nectar = models.PositiveIntegerField(default=0)
    wetland_1 = models.ForeignKey("BirdCard", related_name="Wetland1", on_delete=models.SET_NULL, null=True, blank=True)
    wetland_2 = models.ForeignKey("BirdCard", related_name="Wetland2", on_delete=models.SET_NULL, null=True, blank=True)
    wetland_3 = models.ForeignKey("BirdCard", related_name="Wetland3", on_delete=models.SET_NULL, null=True, blank=True)
    wetland_4 = models.ForeignKey("BirdCard", related_name="Wetland4", on_delete=models.SET_NULL, null=True, blank=True)
    wetland_5 = models.ForeignKey("BirdCard", related_name="Wetland5", on_delete=models.SET_NULL, null=True, blank=True)
    end_of_round_1_goal = models.ForeignKey("EndRoundGoal", related_name="EndRoundGoal1", on_delete=models.SET_DEFAULT, default=EndRoundGoal.create_default_goal)
    end_of_round_2_goal = models.ForeignKey("EndRoundGoal", related_name="EndRoundGoal2", on_delete=models.SET_DEFAULT, default=EndRoundGoal.create_default_goal)
    end_of_round_3_goal = models.ForeignKey("EndRoundGoal", related_name="EndRoundGoal3", on_delete=models.SET_DEFAULT, default=EndRoundGoal.create_default_goal)
    end_of_round_4_goal = models.ForeignKey("EndRoundGoal", related_name="EndRoundGoal4", on_delete=models.SET_DEFAULT, default=EndRoundGoal.create_default_goal)

class Food(models.Model):
    id = models.AutoField(primary_key=True)
    food_name = models.CharField(max_length=6, default="default")

    def __str__(self):
        return self.food_name

class FoodJunction(models.Model):
    card = models.ForeignKey("BirdCard", on_delete=models.CASCADE)
    food = models.ManyToManyField(Food)

    def __str__(self):
        food_str = ""
        for f in self.food.all():
            food_str = food_str + f.food_name + " or "
        food_str = food_str[:-4]
        return self.card.name + " eats " + food_str
    
    class Meta:
        ordering = ['card__name']
