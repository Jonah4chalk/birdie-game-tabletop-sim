from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('board/<int:board_id>', views.board, name='board'),
    path('<str:bird_name>/', views.detail, name='detail'),
    path('board/<int:board_id>/update/<pk>', views.BirdUpdateView.as_view(), name='birdcard_update'),
    path('board/<pk>/add/<str:board_slot>', views.BirdAddView.as_view(), name='bird_add'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)