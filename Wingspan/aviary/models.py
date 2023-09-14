from django.db import models
from django.core.validators import MaxValueValidator
from django.utils.translation import gettext_lazy as _
# Create your models here.

class Ability(models.TextChoices):
    PINK = 'PI', _('Pink')
    YELLOW = 'YE', _('Yellow')
    BROWN = 'BR', _('Brown')
    WHITE = 'WH', _('White')
    BLUE = 'BL', _('Blue')

class Habitat(models.TextChoices):
    FOREST = 'FO', _('Forest')
    GRASSLAND = 'GR', _('Grassland')
    WETLAND = 'WE', _('Wetland')


class Food(models.TextChoices):
    WORM = 'W', _('Worm')
    GRAIN = 'G', _('Grain')
    FISH = 'F', _('Fish')
    CHERRY = 'C', _('Cherry')
    RAT = 'R', _('Rat')
    NECTAR = 'N', _('Nectar')

class BirdCard(models.Model):
    # nest types
    GROUND = 0
    CAVITY = 1
    STICK = 2
    BOWL = 3
    STAR = 4
    NONE = 5

    # ability types
    PINK = 6
    YELLOW = 7
    BROWN = 8
    WHITE = 9
    BLUE = 10

    # habitat types
    FOREST = 11
    GRASSLAND = 12
    WETLAND = 13

    # food types
    WORM = 14
    GRAIN = 15
    FISH = 16
    CHERRY = 17
    RAT = 18
    NECTAR = 19
    WILD = 20

    NEST_TYPE = (
        (GROUND, _("Ground")),
        (CAVITY, _("Cavity")),
        (STICK, _("Stick")),
        (BOWL, _("Bowl")),
        (STAR, _("Star")),
        (NONE, _("None")),
    )
    ABILITY_TYPE = (
        (PINK, _('Pink')),
        (YELLOW, _('Yellow')),
        (BROWN, _('Brown')),
        (WHITE, _('White')),
        (BLUE, _('Blue')),
    )
    name = models.CharField(max_length=50)
    image = models.ImageField()
    nest_size = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(6)])
    # nest_type = models.IntegerField(choices=NEST_TYPE, default=NONE)
    wingspan = models.PositiveIntegerField(default=1)
    # habitats = models.ManyToManyField(Habitat)
    # food_cost = models.ManyToManyField(Food)
    feathers = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(9)])
    ability_desc = models.CharField(max_length=200)
    # ability_type = models.IntegerField(choices=ABILITY_TYPE, default=WHITE)
    cached_food = models.PositiveIntegerField(default=0)
    tucked_cards = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    
class Board(models.Model):
    forest_1 = models.ForeignKey(BirdCard, related_name="Forest1", on_delete=models.SET_NULL, null=True)
    forest_2 = models.ForeignKey(BirdCard, related_name="Forest2", on_delete=models.SET_NULL, null=True)
    forest_3 = models.ForeignKey(BirdCard, related_name="Forest3", on_delete=models.SET_NULL, null=True)
    forest_4 = models.ForeignKey(BirdCard, related_name="Forest4", on_delete=models.SET_NULL, null=True)
    forest_5 = models.ForeignKey(BirdCard, related_name="Forest5", on_delete=models.SET_NULL, null=True)
    grassland_1 = models.ForeignKey(BirdCard, related_name="Grassland1", on_delete=models.SET_NULL, null=True)
    grassland_2 = models.ForeignKey(BirdCard, related_name="Grassland2", on_delete=models.SET_NULL, null=True)
    grassland_3 = models.ForeignKey(BirdCard, related_name="Grassland3", on_delete=models.SET_NULL, null=True)
    grassland_4 = models.ForeignKey(BirdCard, related_name="Grassland4", on_delete=models.SET_NULL, null=True)
    grassland_5 = models.ForeignKey(BirdCard, related_name="Grassland5", on_delete=models.SET_NULL, null=True)
    wetland_1 = models.ForeignKey(BirdCard, related_name="Wetland1", on_delete=models.SET_NULL, null=True)
    wetland_2 = models.ForeignKey(BirdCard, related_name="Wetland2", on_delete=models.SET_NULL, null=True)
    wetland_3 = models.ForeignKey(BirdCard, related_name="Wetland3", on_delete=models.SET_NULL, null=True)
    wetland_4 = models.ForeignKey(BirdCard, related_name="Wetland4", on_delete=models.SET_NULL, null=True)
    wetland_5 = models.ForeignKey(BirdCard, related_name="Wetland5", on_delete=models.SET_NULL, null=True)