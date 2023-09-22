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
    context = {
        "board": board,
    }
    return render(request, "wingspan/board.html", context)