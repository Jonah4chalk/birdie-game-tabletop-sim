from models import BirdCard, BirdCardTemplate, FoodJunction
from collections import defaultdict

def create_bird_scaffold_models():
    counter = 0
    preexisting_cards = BirdCardTemplate.objects.values_list('name', flat=True)
    for birdcard in BirdCard.objects.all():
        if birdcard.name not in preexisting_cards:
            b = BirdCardTemplate(
                name=birdcard.name,
                nest_size=birdcard.nest_size,
                nest_type=birdcard.nest_type,
                wingspan=birdcard.wingspan,
                feathers=birdcard.feathers,
                ability_desc=birdcard.ability_desc,
                ability_type=birdcard.ability_type,
                direction_facing=birdcard.direction_facing,
                habitats=birdcard.habitats,
                first_food=birdcard.first_food,
                second_food=birdcard.second_food,
                third_food=birdcard.third_food,
                costs_one_food=birdcard.costs_one_food
            )
            b.save()
            counter += 1
            print(f'Added {birdcard.name}')
    print(f'Created {counter} templates')
