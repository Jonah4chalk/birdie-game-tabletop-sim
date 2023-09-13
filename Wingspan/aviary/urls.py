from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('board/<int:board_id>', views.board, name='board'),
    path('<int:birdcard_id>/', views.detail, name='detail')
]