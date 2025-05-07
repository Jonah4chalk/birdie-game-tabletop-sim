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
    GOALS = (
        ('No Goal', 'No Goal'),
        ('Eggs in Forest', 'Eggs in Forest'),
        ('Eggs in Grassland', 'Eggs in Grassland'),
        ('Eggs in Wetland', 'Eggs in Wetland'),
        ('Birds in Forest', 'Birds in Forest'),
        ('Birds in Grassland', 'Birds in Grassland'),
        ('Birds in Wetland', 'Birds in Wetland'),
        ('Bird Food Cost', 'Food Cost of Played Birds'),
        ('Worms in Food Cost', 'Worms in Food Cost'),
        ('Cherries and Wheat in Food Cost', 'Cherries and Wheat in Food Cost'),
        ('Fish and Rats in Food Cost', 'Fish and Rats in Food Cost'),
        ('Birds with Tucked Cards', 'Birds with Tucked Cards'),
        ('Brown Birds', 'Brown Birds'),
        ('White Birds', 'White or No Power Birds'),
        ('Eggs in Cavity', 'Eggs in Cavity'),
        ('Eggs in Bowl', 'Eggs in Bowl'),
        ('Eggs in Stick', 'Eggs in Stick'),
        ('Eggs in Ground', 'Eggs in Ground'),
        ('Cavity Birds with Eggs', 'Cavity Birds with Eggs'),
        ('Bowl Birds with Eggs', 'Bowl Birds with Eggs'),
        ('Stick Birds with Eggs', 'Stick Birds with Eggs'),
        ('Ground Birds with Eggs', 'Ground Birds with Eggs'),
        ('Birds with No Eggs', 'Birds with No Eggs'),
        ('Birds worth <4', 'Birds worth <4 points'),
        ('Birds worth >4', 'Birds worth >4 points'),
        ('Food in Personal Supply', 'Food in Personal Supply'),
        ('Bird Cards in Hand', 'Bird Cards in Hand'),
        ('Sets of Eggs', 'Sets of Eggs'),
        ('Filled Columns', 'Filled Columns'),
        ('Birds in a Row', 'Birds in a Row'),
        ('Number of Played Birds', 'Number of Played Birds'),
        ('Beaks Pointing Right', 'Beaks Pointing Right'),
        ('Beaks Pointing Left', 'Beaks Pointing Left'),
        ('Cubes on \"Play a Bird\"', 'Cubes on \"Play a Bird\"'),
    )
    id = models.AutoField(primary_key=True)
    goal = models.CharField(max_length=50, choices=GOALS, default='No Goal')

    def __str__(self):
        return self.goal
    
    def calculate_score(self, board):
        score = 0
        if self.goal == 'No Goal':
            return 0
        elif self.goal == 'Eggs in Forest':
            for bird in board.forest_1.all() + board.forest_2.all() + board.forest_3.all() + board.forest_4.all() + board.forest_5.all():
                score += bird.eggs
        elif self.goal == 'Eggs in Grassland':
            for bird in board.grassland_1.all() + board.grassland_2.all() + board.grassland_3.all() + board.grassland_4.all() + board.grassland_5.all():
                score += bird.eggs
        elif self.goal == 'Eggs in Wetland':
            for bird in board.wetland_1.all() + board.wetland_2.all() + board.wetland_3.all() + board.wetland_4.all() + board.wetland_5.all():
                score += bird.eggs
        elif self.goal == 'Birds in Forest':
            return len(board.forest_1.all() + board.forest_2.all() + board.forest_3.all() + board.forest_4.all() + board.forest_5.all())
        elif self.goal == 'Birds in Grassland':
            return len(board.grassland_1.all() + board.grassland_2.all() + board.grassland_3.all() + board.grassland_4.all() + board.grassland_5.all())
        elif self.goal == 'Birds in Wetland':
            return len(board.wetland_1.all() + board.wetland_2.all() + board.wetland_3.all() + board.wetland_4.all() + board.wetland_5.all())
        elif self.goal == 'Bird Food Cost':
            for bird in board.get_all_birds():
                score += len(FoodJunction.objects.filter(card=bird))
        elif self.goal == 'Worms in Food Cost':
            for bird in board.get_all_birds():
                foods = FoodJunction.objects.filter(card=bird).values_list('food__food_name', flat=True)
                for f in foods:
                    if 'Worm' in f:
                        score += 1
        elif self.goal == 'Cherries and Wheat in Food Cost':
            for bird in board.get_all_birds():
                foods = FoodJunction.objects.filter(card=bird).values_list('food__food_name', flat=True)
                for f in foods:
                    if 'Cherry' in f or 'Wheat' in f:
                        score += 1
        elif self.goal == 'Fish and Rats in Food Cost':
            for bird in board.get_all_birds():
                foods = FoodJunction.objects.filter(card=bird).values_list('food__food_name', flat=True)
                for f in foods:
                    if 'Fish' in f or 'Rat' in f:
                        score += 1
        elif self.goal == 'Birds with Tucked Cards':
            for bird in board.get_all_birds():
                if bird.tucked_cards > 0:
                    score += 1
        elif self.goal == 'Brown Birds':
            for bird in board.get_all_birds():
                if bird.ability_type == 'b':
                    score += 1
        elif self.goal == 'White Birds':
            for bird in board.get_all_birds():
                if bird.ability_type == 'w' or bird.ability_type == 'n':
                    score += 1
        elif self.goal == 'Eggs in Cavity':
            for bird in board.get_all_birds():
                if bird.nest_type == 'c' or bird.nest_type == 'a':
                    score += bird.eggs
        elif self.goal == 'Eggs in Bowl':
            for bird in board.get_all_birds():
                if bird.nest_type == 'b' or bird.nest_type == 'a':
                    score += bird.eggs
        elif self.goal == 'Eggs in Stick':
            for bird in board.get_all_birds():
                if bird.nest_type == 's' or bird.nest_type == 'a':
                    score += bird.eggs
        elif self.goal == 'Eggs in Ground':
            for bird in board.get_all_birds():
                if bird.nest_type == 'g' or bird.nest_type == 'a':
                    score += bird.eggs
        elif self.goal == 'Cavity Birds with Eggs':
            for bird in board.get_all_birds():
                if (bird.nest_type == 'c' or bird.nest_type == 'a') and bird.eggs > 0:
                    score += 1
        elif self.goal == 'Bowl Birds with Eggs':
            for bird in board.get_all_birds():
                if (bird.nest_type == 'b' or bird.nest_type == 'a') and bird.eggs > 0:
                    score += 1
        elif self.goal == 'Stick Birds with Eggs':
            for bird in board.get_all_birds():
                if (bird.nest_type == 's' or bird.nest_type == 'a') and bird.eggs > 0:
                    score += 1
        elif self.goal == 'Ground Birds with Eggs':
            for bird in board.get_all_birds():
                if (bird.nest_type == 'g' or bird.nest_type == 'a') and bird.eggs > 0:
                    score += 1
        elif self.goal == 'Birds with No Eggs':
            for bird in board.get_all_birds():
                if bird.eggs == 0:
                    score += 1
        elif self.goal == 'Birds worth <4':
            for bird in board.get_all_birds():
                if bird.feathers < 4:
                    score += 1
        elif self.goal == 'Birds worth >4':
            for bird in board.get_all_birds():
                if bird.feathers > 4:
                    score += 1
        elif self.goal == 'Food in Personal Supply':
            # placeholder
            score = 0
        elif self.goal == 'Bird Cards in Hand':
            # placeholder
            score = 0
        elif self.goal == 'Sets of Eggs':
            forest_eggs = grassland_eggs = wetland_eggs = 0
            for forest_bird in board.get_forest_birds():
                forest_eggs += forest_bird.eggs
            for grassland_bird in board.get_grassland_birds():
                grassland_eggs += grassland_bird.eggs
            for wetland_bird in board.get_wetland_birds():
                wetland_eggs += wetland_bird.eggs
            score = min(forest_eggs, grassland_eggs, wetland_eggs)
        elif self.goal == 'Filled Columns':
            forest_birds = board.get_forest_birds()
            grassland_birds = board.get_grassland_birds()
            wetland_birds = board.get_wetland_birds()
            score = min(len(forest_birds), len(grassland_birds), len(wetland_birds))
        elif self.goal == 'Birds in a Row':
            forest_birds = board.get_forest_birds()
            grassland_birds = board.get_grassland_birds()
            wetland_birds = board.get_wetland_birds()
            score = max(len(forest_birds), len(grassland_birds), len(wetland_birds))
        elif self.goal == 'Number of Played Birds':
            score = len(board.get_all_birds())
        elif self.goal == 'Beaks Pointing Right':
            for bird in board.get_all_birds():
                if bird.direction_facing == 'r':
                    score += 1
        elif self.goal == 'Beaks Pointing Left':
            for bird in board.get_all_birds():
                if bird.direction_facing == 'l':
                    score += 1
        elif self.goal == 'Cubes on "Play a Bird"':
            # placeholder
            score = 0
        else:
            raise ValidationError("Invalid goal")      
        return score
    
    @classmethod
    def create_default_goal(cls):
        goal = cls.objects.create()
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

    def __str__(self):
        return f"Board {self.pk}"
    
    def get_all_birds(self):
        return list(filter(None, [
            self.forest_1, self.forest_2, self.forest_3, self.forest_4, self.forest_5,
            self.grassland_1, self.grassland_2, self.grassland_3, self.grassland_4, self.grassland_5,
            self.wetland_1, self.wetland_2, self.wetland_3, self.wetland_4, self.wetland_5
        ]))
    
    def get_forest_birds(self):
        return list(filter(None, [
            self.forest_1, self.forest_2, self.forest_3, self.forest_4, self.forest_5
        ]))
    
    def get_grassland_birds(self):
        return list(filter(None, [
            self.grassland_1, self.grassland_2, self.grassland_3, self.grassland_4, self.grassland_5
        ]))
    
    def get_wetland_birds(self):
        return list(filter(None, [
            self.wetland_1, self.wetland_2, self.wetland_3, self.wetland_4, self.wetland_5
        ]))

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

class BonusCard(models.Model):
    BONUSES = (
        ('No Bonus', 'No Bonus'),
        ('Forester', 'Birds that can only live in the forest'), #3-4: 4pts, 5: 8pts
        ('Prairie Manager', 'Birds that can only live in the grassland'), #2-3: 3pts, 4+: 8pts
        ('Wetland Scientist', 'Birds that can only live in the wetland'), #3-4: 3pts, 5: 7pts
        ('Bird Feeder', 'Birds that eat wheat'), # 5-7: 3pts, 8+: 7pts
        ('Food Web Expert', 'Birds that can only eat worms'), # 2pts per bird
        ('Fishery Manager', 'Birds that eat fish'), # 2-3: 3pts, 4: 8pts
        ('Omnivore Expert', 'Birds that eat wild'), # 2pts per bird
        ('Rodentologist', 'Birds that eat rats'), # 2pts per bird
        ('Viticulturalist', 'Birds that eat cherries'), # 2-3: 3pts, 4+: 7pts 
        ('Anatomist', 'Birds with body parts in their names'), # 2-3: 3pts, 4+: 7pts
        ('Cartographer', 'Birds with geographic terms in their names'), # 2-3: 3pts, 4+: 7pts
        ('Historian', 'Birds named after a person'), # 2pts per bird
        ('Photographer', 'Birds with a color in their name'), # 4-5: 3, 6+: 6pts
        ('Breeding Manager', 'Birds that have at least 4 eggs'), # 1pt per bird
        ('Oologist', 'Birds that have at least 1 egg'), # 7-8: 3pts, 9+: 6pts
        ('Enclosure Builder', 'Birds with ground nests'), # 4-5: 4pts, 6+: 7pts
        ('Nest Box Builder', 'Birds with cavity nests'), # 4-5: 4pts, 6+: 7pts
        ('Platform Builder', 'Birds with stick nests'), # 4-5: 4pts, 6+: 7pts
        ('Wildlife Gardener', 'Birds with bowl nests'), # 4-5: 4pts, 6+: 7pts
        ('Backyard Birder', 'Birds worth less than 4 points'), # 5-6: 3pts, 7+: 6pts
        ('Passerine Specialist', 'Birds with wingspan 30cm or less'), # 4-5: 3pts, 6+: 6pts
        ('Large Bird Specialist', 'Birds with wingspan more than 65cm'), # 4-5: 3pts, 6+: 6pts
        ('Bird Counter', 'Birds with a tucking power'), # 2pts per bird
        ('Falconer', 'Birds with a death power'), # 2pts per bird
        ('Ecologist', 'Birds in your habitat with the fewest birds'), # 2pts per bird
        ('Visionary Leader', 'Bird cards in hand at the end of the game'), # 5-7: 4pts, 8+: 7pts
    )
    id = models.AutoField(primary_key=True)
    bonus = models.CharField(max_length=50, choices=BONUSES, default='No Bonus')
    
    def calculate_score(self, board):
        score = 0
        count = 0
        if self.bonus == 'No Bonus':
            return 0
        elif self.bonus == 'Forester':
            forest = Habitat.objects.get(habitat_name='forest')
            grassland = Habitat.objects.get(habitat_name='grassland')
            wetland = Habitat.objects.get(habitat_name='wetland')
            for bird in board.get_forest_birds():
                if bird.habitats.filter(habitat_name=forest.habitat_name).exists() and not bird.habitats.filter(habitat_name=grassland.habitat_name).exists() and not bird.habitats.filter(habitat_name=wetland.habitat_name).exists():
                    count += 1
            if count >= 5:
                score += 8
            elif count >= 3:
                score += 4
        elif self.bonus == 'Prairie Manager':
            forest = Habitat.objects.get(habitat_name='forest')
            grassland = Habitat.objects.get(habitat_name='grassland')
            wetland = Habitat.objects.get(habitat_name='wetland')
            for bird in board.get_grassland_birds():
                if bird.habitats.filter(habitat_name=grassland.habitat_name).exists() and not bird.habitats.filter(habitat_name=forest.habitat_name).exists() and not bird.habitats.filter(habitat_name=wetland.habitat_name).exists():
                    count += 1
            if count >= 5:
                score += 8
            elif count >= 2:
                score += 3
        elif self.bonus == 'Wetland Scientist':
            forest = Habitat.objects.get(habitat_name='forest')
            grassland = Habitat.objects.get(habitat_name='grassland')
            wetland = Habitat.objects.get(habitat_name='wetland')
            for bird in board.get_wetland_birds():
                if bird.habitats.filter(habitat_name=wetland.habitat_name).exists() and not bird.habitats.filter(habitat_name=forest.habitat_name).exists() and not bird.habitats.filter(habitat_name=grassland.habitat_name).exists():
                    count += 1
            if count >= 5:
                score += 7
            elif count >= 3:
                score += 3
        elif self.bonus == 'Bird Feeder':
            for bird in board.get_all_birds():
                if FoodJunction.objects.filter(card=bird, food__food_name='Wheat').exists():
                    count += 1
            if count >= 8:
                score += 7
            elif count >= 5:
                score += 3
        elif self.bonus == 'Food Web Expert':
            for bird in board.get_all_birds():
                if FoodJunction.objects.filter(card=bird, food__food_name='Worm').exists() and not FoodJunction.objects.filter(card=bird, food__food_name='Fish').exists() and not FoodJunction.objects.filter(card=bird, food__food_name='Cherry').exists() and not FoodJunction.objects.filter(card=bird, food__food_name='Rat').exists() and not FoodJunction.objects.filter(card=bird, food__food_name='Nectar').exists() and not FoodJunction.objects.filter(card=bird, food__food_name='Wheat').exists() and not FoodJunction.objects.filter(card=bird, food__food_name='Wild').exists():
                    count += 1
            score += count * 2
        elif self.bonus == 'Fishery Manager':
            for bird in board.get_all_birds():
                if FoodJunction.objects.filter(card=bird, food__food_name='Fish').exists():
                    count += 1
            if count >= 4:
                score += 8
            elif count >= 2:
                score += 3
        elif self.bonus == 'Omnivore Expert':
            for bird in board.get_all_birds():
                if FoodJunction.objects.filter(card=bird, food__food_name='Wild').exists():
                    count += 1
            score += count * 2
        elif self.bonus == 'Rodentologist':
            for bird in board.get_all_birds():
                if FoodJunction.objects.filter(card=bird, food__food_name='Rat').exists():
                    count += 1
            score += count * 2
        elif self.bonus == 'Viticulturalist':
            for bird in board.get_all_birds():
                if FoodJunction.objects.filter(card=bird, food__food_name='Cherry').exists():
                    count += 1
            if count >= 4:
                score += 7
            elif count >= 2:
                score += 3
        elif self.bonus == 'Anatomist':
            for bird in board.get_all_birds():
                if 'back' in bird.name.lower() or 'beak' in bird.name.lower() or 'belly' in bird.name.lower() or 'bill' in bird.name.lower() or 'breast' in bird.name.lower() or 'cap' in bird.name.lower() or 'chin' in bird.name.lower() or 'collar' in bird.name.lower() or 'crest' in bird.name.lower() or 'crown' in bird.name.lower() or 'eye' in bird.name.lower() or 'face' in bird.name.lower() or 'head' in bird.name.lower() or 'leg' in bird.name.lower() or 'neck' in bird.name.lower() or 'rump' in bird.name.lower() or 'shoulder' in bird.name.lower() or 'throat' in bird.name.lower() or 'toe' in bird.name.lower() or 'wing' in bird.name.lower():
                    count += 1
            if count >= 4:
                score += 7
            elif count >= 2:
                score += 3
        elif self.bonus == 'Cartographer':
            for bird in board.get_all_birds():
                if 'american' in bird.name.lower() or 'atlantic' in bird.name.lower() or 'baltimore' in bird.name.lower() or 'california' in bird.name.lower() or 'canada' in bird.name.lower() or 'carolina' in bird.name.lower() or 'chihuahua' in bird.name.lower() or 'eastern' in bird.name.lower() or 'inca' in bird.name.lower() or 'kentucky' in bird.name.lower() or 'mississippi' in bird.name.lower() or 'mountain' in bird.name.lower() or 'northern' in bird.name.lower() or 'sandhill' in bird.name.lower() or 'savannah' in bird.name.lower() or 'western' in bird.name.lower() or 'eurasian' in bird.name.lower() or 'european' in bird.name.lower() or 'corsican' in bird.name.lower() or 'moor' in bird.name.lower() or 'prairie' in bird.name.lower():
                    count += 1
            if count >= 4:
                score += 7
            elif count >= 2:
                score += 3
        elif self.bonus == 'Historian':
            for bird in board.get_all_birds():
                if '\'s' in bird.name:
                    count += 1
            score += count * 2
        elif self.bonus == 'Photographer':
            for bird in board.get_all_birds():
                if 'ash' in bird.name.lower() or 'black' in bird.name.lower() or 'blue' in bird.name.lower() or 'brown' in bird.name.lower() or 'bronze' in bird.name.lower() or 'cerulean' in bird.name.lower() or 'chestnut' in bird.name.lower() or 'ferruginous' in bird.name.lower() or 'gold' in bird.name.lower() or 'gray' in bird.name.lower() or 'green' in bird.name.lower() or 'indigo' in bird.name.lower() or 'lazuli' in bird.name.lower() or 'purple' in bird.name.lower() or 'red' in bird.name.lower() or 'rose' in bird.name.lower() or 'roseate' in bird.name.lower() or 'ruby' in bird.name.lower() or 'ruddy' in bird.name.lower() or 'rufous' in bird.name.lower() or 'snowy' in bird.name.lower() or 'white' in bird.name.lower() or 'yellow' in bird.name.lower():
                    count += 1
            if count >= 6:
                score += 6
            elif count >= 4:
                score += 3
        elif self.bonus == 'Breeding Manager':
            for bird in board.get_all_birds():
                if bird.eggs >= 4:
                    count += 1
            score += count
        elif self.bonus == 'Oologist':
            for bird in board.get_all_birds():
                if bird.eggs >= 1:
                    count += 1
            if count >= 9:
                score += 6
            elif count >= 7:
                score += 3
        elif self.bonus == 'Enclosure Builder':
            for bird in board.get_all_birds():
                if bird.nest_type == 'g' or bird.nest_type == 'a':
                    count += 1
            if count >= 6:
                score += 7
            elif count >= 4:
                score += 4
        elif self.bonus == 'Nest Box Builder':
            for bird in board.get_all_birds():
                if bird.nest_type == 'c' or bird.nest_type == 'a':
                    count += 1
            if count >= 6:
                score += 7
            elif count >= 4:
                score += 4
        elif self.bonus == 'Platform Builder':
            for bird in board.get_all_birds():
                if bird.nest_type == 's' or bird.nest_type == 'a':
                    count += 1
            if count >= 6:
                score += 7
            elif count >= 4:
                score += 4
        elif self.bonus == 'Wildlife Gardener':
            for bird in board.get_all_birds():
                if bird.nest_type == 'b' or bird.nest_type == 'a':
                    count += 1
            if count >= 6:
                score += 7
            elif count >= 4:
                score += 4
        elif self.bonus == 'Backyard Birder':
            for bird in board.get_all_birds():
                if bird.feathers < 4:
                    count += 1
            if count >= 7:
                score += 6
            elif count >= 5:
                score += 3
        elif self.bonus == 'Passerine Specialist':
            for bird in board.get_all_birds():
                if bird.wingspan <= 30:
                    count += 1
            if count >= 6:
                score += 6
            elif count >= 4:
                score += 3
        elif self.bonus == 'Large Bird Specialist':
            for bird in board.get_all_birds():
                if bird.wingspan >= 65:
                    count += 1
            if count >= 6:
                score += 6
            elif count >= 4:
                score += 3
        elif self.bonus == 'Bird Counter':
            for bird in board.get_all_birds():
                if bird.tucked_cards > 0:
                    count += 1
            score += count * 2
        elif self.bonus == 'Falconer':
            for bird in board.get_all_birds():
                if "[Death]" in bird.ability_desc:
                    count += 1
            score += count * 2
        elif self.bonus == 'Ecologist':
            forest_birds = board.get_forest_birds()
            grassland_birds = board.get_grassland_birds()
            wetland_birds = board.get_wetland_birds()
            count = min(len(forest_birds), len(grassland_birds), len(wetland_birds))
            score += count * 2
        elif self.bonus == 'Visionary Leader':
            # placeholder
            score = 0
        else:
            raise ValidationError("Invalid bonus")
        return score