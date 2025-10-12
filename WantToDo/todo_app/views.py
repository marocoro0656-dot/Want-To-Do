from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Want
from .forms import FilterForm, WantForm

def ryofunamoto(request):
    return render(
        request, 'todo_app/ryofunamoto.html'
    )

def home(request):
    form = FilterForm(request.GET or None)
    return render(request, 'todo/home.html', {'form': form})


@login_required
def home(request):
    # フィルタフォーム（GET）
    form = FilterForm(request.GET or None)

    qs = Want.objects.filter(user=request.user, done=False)  # 未完のみ
    if form.is_valid():
        category   = form.cleaned_data.get('category')
        difficulty = form.cleaned_data.get('difficulty')
        start_date = form.cleaned_data.get('start_date')  # 期限の下限
        end_date   = form.cleaned_data.get('end_date')    # 期限の上限

        if category:
            qs = qs.filter(category=category)
        if difficulty:
            qs = qs.filter(difficulty=difficulty)
        if start_date:
            qs = qs.filter(deadline__gte=start_date)
        if end_date:
            qs = qs.filter(deadline__lte=end_date)

    # 期限が近い順に4件（未完のみ）
    upcoming = qs.order_by('deadline', '-updated_at')[:4]

    return render(request, 'todo/home.html', {
        'form': form,
        'upcoming': upcoming,
    })

@login_required
def add_want(request):
    if request.method == 'POST':
        form = WantForm(request.POST)
        if form.is_valid():
            want = form.save(commit=False)
            want.user = request.user
            want.save()
            messages.success(request, 'WantToDo を作成しました。')
            return redirect('todo_app:home')
    else:
        form = WantForm()
    return render(request, 'todo/add_want.html', {'form': form})

@login_required
def incomplete_list(request):
    qs = Want.objects.filter(user=request.user, done=False).order_by('deadline', '-updated_at')
    return render(request, 'todo/incomplete_list.html', {'wants': qs})

@login_required
def done_list(request):
    # 実装例：ログインユーザーの完了済みのみを取得して渡す
    # wants = Want.objects.filter(user=request.user, done=True).order_by('-updated_at')
    wants = []  # まずは空で仮運用
    return render(request, 'todo/done_list.html', {'wants': wants})