from django.shortcuts import render

def ryofunamoto(request):
    return render(
        request, 'todo_app/ryofunamoto.html'
    )
