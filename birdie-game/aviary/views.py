import json
from django.shortcuts import redirect, render
from django.template import loader
from .models import BirdCard, Board, EndRoundGoal
from django.http import Http404, JsonResponse
from django.views.generic.edit import UpdateView, FormView
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
        "tucked_cards",
        "eggs"
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

def end_of_round_goals(request, pk):
    board = Board.objects.get(pk=pk)
    # update scores of goals before rendering
    for goal in [
        board.end_of_round_1_goal,
        board.end_of_round_2_goal,
        board.end_of_round_3_goal,
        board.end_of_round_4_goal
    ]:
        goal.score = goal.calculate_score(board)
        goal.save()
    return render(request, 'aviary/end_of_round_goals.html', {'board': board, 'EndRoundGoal': EndRoundGoal})

def update_end_of_round_goals(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        rounds = data.get('rounds') # array of rounds to be edited
        goals = data.get('goals') # must be length 4 containing new goals for rounds 1-4
        board_id = data.get('board_id')

        try:
            board = Board.objects.get(pk=board_id)

            if 'round-1' in rounds:
                board.end_of_round_1_goal.goal = EndRoundGoal.GOALS[goals[0]]
                board.end_of_round_1_goal.score = board.end_of_round_1_goal.calculate_score(board)
                board.end_of_round_1_goal.save()
            elif 'round-2' in rounds:
                board.end_of_round_2_goal.goal = EndRoundGoal.GOALS[goals[1]]
                board.end_of_round_2_goal.score = board.end_of_round_2_goal.calculate_score(board)
                board.end_of_round_2_goal.save()
            elif 'round-3' in rounds:
                board.end_of_round_3_goal.goal = EndRoundGoal.GOALS[goals[2]]
                board.end_of_round_3_goal.score = board.end_of_round_3_goal.calculate_score(board)
                board.end_of_round_3_goal.save()
            elif 'round-4' in rounds:
                board.end_of_round_4_goal.goal = EndRoundGoal.GOALS[goals[3]]
                board.end_of_round_4_goal.score = board.end_of_round_4_goal.calculate_score(board)
                board.end_of_round_4_goal.save()

            board.save()
            return JsonResponse({
                'status': 'success',
                'goals': [
                    board.end_of_round_1_goal.goal,
                    board.end_of_round_2_goal.goal, 
                    board.end_of_round_3_goal.goal,
                    board.end_of_round_4_goal.goal
                ],
                'scores': [
                    board.end_of_round_1_goal.score,
                    board.end_of_round_2_goal.score,
                    board.end_of_round_3_goal.score,
                    board.end_of_round_4_goal.score
                ]
            })

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
            