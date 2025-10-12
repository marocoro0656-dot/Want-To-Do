from django.urls import path, include
from . import views

app_name = 'todo_app'

urlpatterns = [
    path('ryofunamoto/', views.ryofunamoto, name='ryofunamoto'),
    path('', views.home, name='home'),  
    path('add/', views.add_want, name='add_want'),  # 新規作成ページ（未実装）
    path('incomplete/', views.incomplete_list, name='incomplete_list'),  # 未完了一覧（未実装）
    path('done/', views.done_list, name='done_list'),
    
    ]
