from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('board/<int:board_id>', views.board, name='board'),
    path('<int:birdcard_id>/', views.detail, name='detail')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)