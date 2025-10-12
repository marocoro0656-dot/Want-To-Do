from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Want
from .forms import FilterForm, WantForm
from django.utils import timezone

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
            messages.success(request, 'WantToDoを登録しました。')
            return redirect('todo_app:incomplete_list')  # ← 成功時遷移
        else:
            # 必須漏れなど
            messages.error(request, '入力内容に不備があります。各項目のエラーをご確認ください。')
    else:
        form = WantForm()

    return render(request, 'todo/add_want.html', {'form': form})

@login_required
def incomplete_list(request):
    qs = Want.objects.filter(user=request.user, done=False).order_by('deadline', '-updated_at')
    paginator = Paginator(qs, 10)  # 1ページ=10件
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'todo/incomplete_list.html', {
        'page_obj': page_obj,
        'wants': page_obj.object_list,  # テンプレで使いやすく
    })

@login_required
@require_POST
def complete_want(request, pk):
    want = get_object_or_404(Want, pk=pk, user=request.user, done=False)
    want.done = True
    want.completed_at = timezone.now()         # ← ここで完了日時をセット
    want.save()
    messages.success(request, '完了にしました。')
    next_url = request.POST.get('next') or 'todo_app:incomplete_list'
    return redirect(next_url)

@login_required
def done_list(request):
    qs = (Want.objects
          .filter(user=request.user, done=True)
          .order_by('-deadline', '-completed_at', '-updated_at'))
    paginator = Paginator(qs, 10)  # 必要ならページング（任意）
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'todo/done_list.html', {
        'wants': page_obj.object_list,
        'page_obj': page_obj,
    })