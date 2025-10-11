from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def ryofunamoto(request):
    return render(
        request, 'todo_app/ryofunamoto.html'
    )

@login_required
def home(request):
    return render(request, 'todo/home.html')

def done_list(request):
    # 実装例：ログインユーザーの完了済みのみを取得して渡す
    # wants = Want.objects.filter(user=request.user, done=True).order_by('-updated_at')
    wants = []  # まずは空で仮運用
    return render(request, 'todo/done_list.html', {'wants': wants})