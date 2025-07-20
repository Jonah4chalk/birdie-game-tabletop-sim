from aviary.models import FoodJunction, BirdCard
from collections import defaultdict
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Sets the first food, second food, third food, and costs_one_food fields of bird cards"

    def handle(self, *args, **options):
        birds: defaultdict[str, list[FoodJunction]] = defaultdict(list)
        for obj in FoodJunction.objects.select_related("card").all():
            birds[obj.card].append(obj)
        for bird, fj in birds.items():
            card: BirdCard = fj[0].card
            food_count = 0
            for j in fj:
                if len(j.food.all()) > 1:
                    # only case is when the bird only needs one food
                    card.costs_one_food = True
                for f in j.food.all():
                    if food_count == 0:
                        card.first_food = f
                    elif food_count == 1:
                        card.second_food = f
                    elif food_count == 2:
                        card.third_food = f
                    food_count += 1
            card.save()
                    

        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {len(birds).keys()} birds')
        )