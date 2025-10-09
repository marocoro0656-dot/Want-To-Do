from django.urls import path
from . import views

app_name = 'todo_app'

urlpatterns = [
    path('ryofunamoto/', views.ryofunamoto, name='ryofunamoto'),
    
    ]
