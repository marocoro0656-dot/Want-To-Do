from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from . import views
from .views import MyPasswordChangeView

app_name = 'user'

urlpatterns = [
    path('regist/', views.regist, name='regist'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='user:login'), name='logout'),
    
    # ログアウト（POST推奨）
    path('logout/', auth_views.LogoutView.as_view(next_page='user:login'), name='logout'),
    
    # メールアドレス変更（自作）
    path('email/change/', views.email_change, name='email_change'),

    # パスワード変更（ログイン必須）
    path('password/change/', MyPasswordChangeView.as_view(), name='password_change'),
    path('password/change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='user/password_change_done.html'),
         name='password_change_done'),
    ]
