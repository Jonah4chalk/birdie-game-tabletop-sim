from django.contrib import admin
from .models import BirdCard, EndRoundGoal, Habitat, Food, Board, FoodJunction
# Register your models here.

admin.site.register(BirdCard)
admin.site.register(Board)
admin.site.register(Habitat)
admin.site.register(Food)
admin.site.register(FoodJunction)
admin.site.register(EndRoundGoal)