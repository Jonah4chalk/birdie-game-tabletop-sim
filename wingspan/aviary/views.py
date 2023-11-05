from django.shortcuts import redirect, render
from django.template import loader
from .models import BirdCard, Board
from django.http import Http404
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django import forms

# Create your views here.
from django.http import HttpResponse


def index(request):
    return render(request, "aviary/index.html", {})

def detail(request, bird_name):
    try:
        birdcard = BirdCard.objects.get(name=bird_name)
    except BirdCard.DoesNotExist:
        raise Http404("Detail: BirdCard does not exist")
    
    context = {"birdcard": birdcard}
    return render(request, "aviary/detail.html", context)

def board(request, pk):
    try:
        board = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        raise Http404("Board does not exist")
    context = {
        "board": board,
    }
    return render(request, "aviary/board.html", context)

class BirdUpdateView(UpdateView):
    model = BirdCard
    fields = [
        "cached_food",
        "tucked_cards"
    ]
    template_name_suffix = "_update"
    def get_success_url(self) -> str:
        board_pk = self.kwargs["board_id"]
        return reverse_lazy("board", kwargs={"pk": board_pk})
    
class BirdAddModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BirdAddModelForm, self).__init__(*args, **kwargs)
        field_name = kwargs.pop('board_slot', None)
        if field_name:
            for field in self.fields.copy():
                if field != field_name:
                    del self.fields[field]

    class Meta:
        model = Board
        exclude = ()
    
class BirdAddView(UpdateView):
    model = Board
    form_class = BirdAddModelForm
    template_name = "aviary/bird_add.html"
    def get_success_url(self) -> str:
        board_pk = self.kwargs["pk"]
        return reverse_lazy("board", kwargs={"pk": board_pk})

def create_board(request):
    new_board = Board.objects.create()
    return redirect('board', pk=new_board.pk)