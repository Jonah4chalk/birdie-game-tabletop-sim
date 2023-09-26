from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('board/<int:board_id>', views.board, name='board'),
    path('<str:bird_name>/', views.detail, name='detail'),
    path(r'^update/(?P<pk>\d+)', views.BirdUpdateView.as_view(), name='birdcard_update')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)