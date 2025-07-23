import json
from django.shortcuts import get_object_or_404, redirect, render
from .models import BirdCard, BirdCardTemplate, Board, BonusCard, BonusCardAddForm, EndRoundGoal, BoardUpdateForm
from django.http import Http404, JsonResponse
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
        exclude = ("end_of_round_1_goal", "end_of_round_2_goal", "end_of_round_3_goal", "end_of_round_4_goal", "bonus_cards")
    
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
            
def bonus_cards(request, pk):
    board = Board.objects.get(pk=pk)

    # update scores of current bonus cards before rendering
    for card in board.bonus_cards.all():
        card.score = card.calculate_score(board)
        card.save()
    # render webpage
    return render(request, 'aviary/bonus_cards.html', {'board': board, 'BonusCard': BonusCard})

def add_bonus_card(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = BonusCardAddForm(request.POST)
        if form.is_valid():
            bonus_card = form.save()
            board.bonus_cards.add(bonus_card)
            return redirect('bonus_cards', pk=pk)
    else:
        form = BonusCardAddForm()
    return render(request, 'aviary/add_bonus_card.html', {'form': form, 'board': board})

def delete_bonus_card(request, board_pk, card_pk):
    board = get_object_or_404(Board, pk=board_pk)
    bonus_card = get_object_or_404(BonusCard, pk=card_pk)
    board.bonus_cards.remove(bonus_card)
    bonus_card.delete()
    return redirect('bonus_cards', pk=board_pk)

def update_bonus_card(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        board_pk = data.get('board_pk')
        card_pk = data.get('card_pk')
        board = get_object_or_404(Board, id=board_pk)
        bonus_card = get_object_or_404(BonusCard, id=card_pk)
        bonus_card.bonus = data.get('bonus')
        bonus_card.score = bonus_card.calculate_score(board)
        bonus_card.save()
        return JsonResponse({
            'status': 'success',
            'bonus_title': bonus_card.bonus,
            'bonus_description': BonusCard.BONUSES[bonus_card.bonus],
            'score': bonus_card.score
        })
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method: ' + request.method}, status=400)
    
def update_board(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = BoardUpdateForm(request.POST)
        if form.is_valid():
            for field, value in form.cleaned_data.items():
                if 'nectar' in field:
                    setattr(board, field, value)
                else:
                    # handle bird card
                    # if bird card didn't change, a bird card should not be created
                    original_bird = getattr(board, field, None)
                    if (getattr(original_bird, 'name', None) == value):
                        continue
                    elif not value:
                        setattr(board, field, None)
                        original_bird.delete()
                    else:
                        # otherwise, create a new bird card
                        template = BirdCardTemplate.objects.get(name=value)
                        new_bird = BirdCard.objects.create(
                            name=value,
                            nest_size=template.nest_size,
                            nest_type=template.nest_type,
                            wingspan=template.wingspan,
                            habitats=template.habitats,
                            feathers=template.feathers,
                            ability_desc=template.ability_desc,
                            ability_type=template.ability_type,
                            direction_facing=template.direction_facing,
                            first_food=template.first_food,
                            second_food=template.second_food,
                            third_food=template.third_food,
                            costs_one_food=template.costs_one_food,
                        )
                        # add the new bird card to the space on the board
                        setattr(board, field, new_bird)
            board.save()
            return reverse_lazy("board", kwargs={"pk": pk})
    else:
        form = BoardUpdateForm(instance=board)

    return None

def edit_cube_count(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        board_pk = data.get('board_id')
        action = data.get('action')
        value = data.get('value')
        board = get_object_or_404(Board, pk=board_pk)
        if action == 'play-a-bird':
            board.play_a_bird_cubes += value
        elif action == 'gain-food':
            board.gain_food_cubes += value
        elif action == 'lay-eggs':
            board.lay_eggs_cubes += value
        elif action == 'draw-bird-cards':
            board.draw_bird_cards_cubes += value
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid action'}, status=422)
        board.save()
        return JsonResponse({
            'status': 'success',
            'values': [
                board.play_a_bird_cubes,
                board.gain_food_cubes,
                board.lay_eggs_cubes,
                board.draw_bird_cards_cubes
            ]}
        )
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method: ' + request.method}, status=400)
        
def edit_nectar_count(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        board_pk = data.get('board_id')
        habitat = data.get('habitat')
        value = data.get('value')
        board = get_object_or_404(Board, pk=board_pk)
        if habitat == 'forest':
            board.forest_nectar += value
        elif habitat == 'grassland':
            board.grassland_nectar += value
        elif habitat == 'wetland':
            board.wetland_nectar += value
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid habitat'}, status=422)
        board.save()
        return JsonResponse({
            'status': 'success',
            'values': [
                board.forest_nectar,
                board.grassland_nectar,
                board.wetland_nectar
            ]}
        )
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method: ' + request.method}, status=400)