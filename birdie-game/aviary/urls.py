from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('update-goals/', views.update_end_of_round_goals, name='update_end_of_round_goals'),
    path('board/<int:pk>/', views.board, name='board'),
    path('<str:bird_name>/', views.detail, name='detail'),
    path('board/<int:board_id>/update/<pk>/', views.BirdUpdateView.as_view(), name='birdcard_update'),
    path('board/<pk>/add/', views.BirdAddView.as_view(), name='bird_add'),
    path('board/create/', views.create_board, name='create_board'),
    path('board/<pk>/goals/', views.end_of_round_goals, name='end_of_round_goals'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)