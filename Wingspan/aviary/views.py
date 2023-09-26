from django.shortcuts import render
from django.template import loader
from .models import BirdCard, Board
from django.http import Http404
from django.views.generic.edit import UpdateView

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the aviary.")

def detail(request, bird_name):
    try:
        birdcard = BirdCard.objects.get(name=bird_name)
    except BirdCard.DoesNotExist:
        raise Http404("Detail: BirdCard does not exist")
    
    context = {"birdcard": birdcard}
    return render(request, "wingspan/detail.html", context)

def board(request, board_id):
    try:
        board = Board.objects.get(pk=board_id)
    except Board.DoesNotExist:
        raise Http404("Board does not exist")
    context = {
        "board": board,
    }
    return render(request, "wingspan/board.html", context)

class BirdUpdateView(UpdateView):
    model = BirdCard
    fields = [
        "cached_food",
        "tucked_cards"
    ]
    template_name_suffix = "_update"