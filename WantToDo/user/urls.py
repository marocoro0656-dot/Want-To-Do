from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('list/', views.user_list, name='user_list'),
    path('regist/', views.regist, name='regist'),
    path('login/', views.login_view, name='login'),

]
