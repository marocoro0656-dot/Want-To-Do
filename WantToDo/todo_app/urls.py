from django.urls import path, include
from . import views
from .views import WantUpdateView, DoneWantDetailView, revert_want, delete_want

app_name = 'todo_app'

urlpatterns = [
    path('ryofunamoto/', views.ryofunamoto, name='ryofunamoto'),
    path('', views.home, name='home'),  
    path('add/', views.add_want, name='add_want'),  # 新規作成ページ
    path('incomplete/', views.incomplete_list, name='incomplete_list'),  # 未完了一覧
    path('done/', views.done_list, name='done_list'),
    path('complete/<int:pk>/', views.complete_want, name='complete_want'),
    path('detail/<int:pk>/', views.want_detail, name='detail'),
    path('delete/<int:pk>/', views.delete_want, name='delete_want'),
    path("want/<int:pk>/edit/", WantUpdateView.as_view(), name="edit"),
    path("done/<int:pk>/", DoneWantDetailView.as_view(), name="done_detail"),
    path("done/<int:pk>/", DoneWantDetailView.as_view(), name="done_detail"),
    path("want/<int:pk>/revert/", revert_want, name="revert_want"),
    path("want/<int:pk>/delete/", delete_want, name="delete_want"),  


    ]
