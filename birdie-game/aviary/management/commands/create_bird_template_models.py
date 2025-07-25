from django.core.management.base import BaseCommand
from aviary.models import BirdCard, BirdCardTemplate

class Command(BaseCommand):
    help = "Create a bird card template for each unique bird card"

    def handle(self, *args, **options):
        birds = BirdCard.objects.order_by('name')
        known = BirdCardTemplate.objects.values_list('name').distinct()
        seen = set()
        for b in birds:
            if b.name not in seen and b.name not in known:
                seen.add(b.name)
                template = BirdCardTemplate(
                    name=b.name,
                    nest_size=b.nest_size,
                    nest_type=b.nest_type,
                    wingspan=b.wingspan,
                    feathers=b.feathers,
                    ability_desc=b.ability_desc,
                    ability_type=b.ability_type,
                    direction_facing=b.direction_facing,
                    first_food=b.first_food,
                    second_food=b.second_food,
                    third_food=b.third_food,
                    costs_one_food=b.costs_one_food
                )
                template.save()
                template.habitats.set(b.habitats.all())
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(seen)} templates'))