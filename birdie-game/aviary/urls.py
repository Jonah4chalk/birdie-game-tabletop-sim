from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('update-goals/', views.update_end_of_round_goals, name='update_end_of_round_goals'),
    path('edit_cube_count/', views.edit_cube_count, name='edit_cube_count'),
    path('edit_nectar_count/', views.edit_nectar_count, name='edit_nectar_count'),
    path('board/<int:pk>/', views.board, name='board'),
    path('<str:bird_name>/', views.detail, name='detail'),
    path('board/<int:board_id>/update/<pk>/', views.BirdUpdateView.as_view(), name='birdcard_update'),
    path('board/<pk>/add/', views.update_board, name='update_board'),
    path('board/create/', views.create_board, name='create_board'),
    path('board/<pk>/goals/', views.end_of_round_goals, name='end_of_round_goals'),
    path('board/<pk>/bonus-cards/view/', views.bonus_cards, name='bonus_cards'),
    path('board/<pk>/bonus-cards/add/', views.add_bonus_card, name='add_bonus_card'),
    path('board/<board_pk>/bonus-cards/<card_pk>/delete/', views.delete_bonus_card, name='delete_bonus_card'),
    path('board/bonus-cards/update', views.update_bonus_card, name='update_bonus_card'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)