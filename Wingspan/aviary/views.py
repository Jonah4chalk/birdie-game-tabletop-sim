from django.shortcuts import render
from django.template import loader
from .models import BirdCard, Board, FoodJunction
from django.http import Http404

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the aviary.")

def detail(request, birdcard_id):
    try:
        birdcard = BirdCard.objects.get(pk=birdcard_id)
    except BirdCard.DoesNotExist:
        raise Http404("BirdCard does not exist")
    
    response = "You're looking at %s"
    return HttpResponse(response % birdcard)

def board(request, board_id):
    try:
        board = Board.objects.get(pk=board_id)
    except Board.DoesNotExist:
        raise Http404("Board does not exist")
    try:
        f1_food = []
        f1_query = FoodJunction.objects.filter(card_id=board.forest_1.id)
        for row in f1_query:
            options = []
            for f in row.food.all():
                options.append(f.food_name)
            f1_food.append(options)
                
    except FoodJunction.DoesNotExist:
        # this bird does not need food to be played, pass nothing
        f1_food = []
        
    context = {
        "board": board,
        "f1_food": f1_food,
    }
    return render(request, "wingspan/index.html", context)