from django.urls import path
from django.conf import settings
from . import views
app_name = "chat"

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
] 
