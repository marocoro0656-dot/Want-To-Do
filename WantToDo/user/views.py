from django.shortcuts import render
from .forms import UserForm

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