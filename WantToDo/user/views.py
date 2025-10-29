from django.shortcuts import render, redirect
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django import forms

from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView

from .forms import SignUpForm, LoginForm, CustomPasswordChangeForm, EmailChangeForm



def regist(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # ユーザー作成
            # 🔽 ここで自動ログイン
            auth_login(request, user)
            messages.success(request, f'ようこそ、{user.username} さん！')
            return redirect('todo_app:home')
        else:
            messages.error(request, '入力内容に誤りがあります。各項目のエラーを確認してください。')
    else:
        form = SignUpForm()

    return render(request, 'user/registration.html', {'user_form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # メール→username へ解決して認証
            user_obj = User.objects.filter(email=email).first()
            user = authenticate(
                request,
                username=(user_obj.username if user_obj else None),
                password=password
            )

            if user is not None:
                auth_login(request, user)
                return redirect('todo_app:home')
            else:
                messages.error(request, 'メールアドレスまたはパスワードが正しくありません。')
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'login_form': form})




@login_required
def email_change(request):
    if request.method == 'POST':
        form = EmailChangeForm(request.POST,  user=request.user)
        if form.is_valid():
            new_email = form.cleaned_data['email']
            request.user.email = new_email
            request.user.save()
            messages.success(request, 'メールアドレスを更新しました。')
            return redirect('todo_app:home')
    else:
        form = EmailChangeForm(user=request.user)

    return render(request, 'user/email_change.html', {'form': form})




#パスワード変更
class PasswordChangeViewCustom(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'user/password_change.html'
    success_url = reverse_lazy('todo_app:home')  # ← 成功時はホームへ
    def form_valid(self, form):
        messages.success(self.request, 'パスワードを変更しました。')
        return super().form_valid(form)