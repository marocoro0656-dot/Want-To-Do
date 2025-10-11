from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'user'

urlpatterns = [
    path('regist/', views.regist, name='regist'),
    path('login/', views.login_view, name='login'),
    
    # ログアウト（POST推奨）
    path('logout/', auth_views.LogoutView.as_view(next_page='user:login'), name='logout'),

    # パスワード変更（ログイン必須）
    path('password/change/',
         auth_views.PasswordChangeView.as_view(
             template_name='user/password_change.html',
             success_url='/user/password/change/done/'  # or reverse_lazy('user:password_change_done')
         ),
         name='password_change'),
    path('password/change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='user/password_change_done.html'),
         name='password_change_done'),

    # メールアドレス変更（自作）
    path('email/change/', views.email_change, name='email_change'),
]
