from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Want
from .forms import FilterForm, WantForm
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import UpdateView, DetailView


def ryofunamoto(request):
    return render(
        request, 'todo_app/ryofunamoto.html'
    )

def home(request):
    form = FilterForm(request.GET or None)
    return render(request, 'todo/home.html', {'form': form})


@login_required
def home(request):
    form = FilterForm(request.GET or None)

    qs = Want.objects.filter(user=request.user, done=False)  # 未完のみ

    # 検索条件があれば適用（= フィルタ中）
    if form.is_valid():
        category   = form.cleaned_data.get('category')
        difficulty = form.cleaned_data.get('difficulty')
        start_date = form.cleaned_data.get('start_date')
        end_date   = form.cleaned_data.get('end_date')

        if category:
            qs = qs.filter(category=category)
        if difficulty:
            qs = qs.filter(difficulty=difficulty)
        if start_date:
            qs = qs.filter(deadline__gte=start_date)
        if end_date:
            qs = qs.filter(deadline__lte=end_date)

        # 検索結果はすべて表示（期限昇順）
        upcoming = qs.order_by('deadline', '-updated_at')

    else:
        # 初期表示は4件まで
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
    return redirect(request.POST.get('next') or 'todo_app:done_list')

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

@login_required
def want_detail(request, pk):
    done=False
    want = get_object_or_404(Want, pk=pk, user=request.user)
    return render(request, 'todo/detail.html', {'w': want})

@login_required
@require_POST
def delete_want(request, pk):
    want = get_object_or_404(Want, pk=pk, user=request.user)
    title = want.title
    want.delete()
    messages.success(request, f'「{title}」を削除しました。')
    # 削除後は未完了一覧へ
    return redirect('todo_app:incomplete_list')

class WantUpdateView(LoginRequiredMixin, UpdateView):
    model = Want
    form_class = WantForm
    template_name = "todo/want_edit.html"

    # 自分のデータ以外は編集できない
    def get_queryset(self):
        return Want.objects.filter(user=self.request.user)

    # 保存後は詳細へ戻す
    def get_success_url(self):
        return reverse("todo_app:detail", kwargs={"pk": self.object.pk})

class DoneWantDetailView(LoginRequiredMixin, DetailView):
    model = Want
    template_name = "todo/done_detail.html"   # 作るテンプレ名
    context_object_name = "w"

    # 自分のアイテム ＆ 完了済み（done=True）のみ表示
    def get_queryset(self):
        return Want.objects.filter(user=self.request.user, done=True)

@login_required
@require_POST
def revert_want(request, pk):
    w = get_object_or_404(Want, pk=pk, user=request.user, done=True)
    w.done = False
    w.save(update_fields=["done", "updated_at"])
    messages.success(request, "1件未完了にしました")
    next_url = request.POST.get("next") or reverse("todo_app:done_list")
    return redirect(next_url)

@login_required
@require_POST
def delete_want(request, pk):
    w = get_object_or_404(Want, pk=pk, user=request.user)
    w.delete()
    messages.success(request, "1件削除しました")
    next_url = request.POST.get("next") or reverse("todo_app:done_list")
    return redirect(next_url)