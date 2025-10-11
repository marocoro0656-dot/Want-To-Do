from django.urls import path, include
from . import views

app_name = 'todo_app'

urlpatterns = [
    path('ryofunamoto/', views.ryofunamoto, name='ryofunamoto'),
    path('', views.home, name='home'),  
    path('done/', views.done_list, name='done_list'),
    
    ]
