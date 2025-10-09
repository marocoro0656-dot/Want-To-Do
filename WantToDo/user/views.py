from django.shortcuts import render
from .forms import UserForm, UserLoginForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout




def user_list(request):
    return render(
        request, 'user/user_list.html'
    )
    
def regist(request):
    user_form = UserForm(request.POST or None)
    if user_form.is_valid():
        user = user_form.save(commit=False)
        
    return render(request, 'user/registration.html', context={
        'user_form': user_form,
    })
    
def login_view(request):
    login_form = UserLoginForm(request.POST or None)
    if login_form.is_valid():
        username = login_form.cleaned_data.get('username')
        password = login_form.cleaned_data.get('password1')
        user = authenticate(request, username=username, password=password)
    return render(request, 'user/login.html', context={
        'login_form': login_form,
    })