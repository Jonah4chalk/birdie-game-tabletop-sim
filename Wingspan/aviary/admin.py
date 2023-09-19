from django.contrib import admin
from .models import BirdCard, Habitat, Food, Board
# Register your models here.

admin.site.register(BirdCard)
admin.site.register(Board)
admin.site.register(Habitat)
admin.site.register(Food)