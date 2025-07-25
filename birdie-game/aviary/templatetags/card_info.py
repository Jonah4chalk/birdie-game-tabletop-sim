from aviary.models import BirdCard, FoodJunction
from django import template
register = template.Library()
from django.http import Http404

@register.inclusion_tag("../templates/aviary/birdcard.html")
def card_info(bird_pk):
    try:
        birdcard = BirdCard.objects.get(pk=bird_pk)
    except BirdCard.DoesNotExist:
        return {
            "bird": None,
            "food": []
        }
    food = []
    try:
        q = FoodJunction.objects.filter(card_id=birdcard.id)
        for row in q:
            options = []
            for f in row.food.all():
                options.append(f.food_name)
            food.append(options)
    except FoodJunction.DoesNotExist:
        # do nothing
        pass
    return {
        "bird": birdcard,
        "food": food
    }
    