from django.db import models
from django.contrib.auth.models import User

class Want(models.Model):
    CATEGORY_CHOICES = [
        ('travel', '外出（旅行）'),
        ('shopping', 'ショッピング'),
        ('hobby', '趣味'),
        ('other', 'その他'),
    ]
    DIFFICULTY_CHOICES = [
        ('high', '高'),
        ('medium', '中'),
        ('low', '低'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wants')
    title = models.CharField('タイトル', max_length=120)
    category = models.CharField('カテゴリ', max_length=20, choices=CATEGORY_CHOICES, blank=True)   # フォーム側で必須化
    difficulty = models.CharField('難易度', max_length=10, choices=DIFFICULTY_CHOICES, blank=True) # フォーム側で必須化
    deadline = models.DateField('期限', null=True, blank=True)  # 任意
    memo = models.CharField('メモ', max_length=120, blank=True) # ← 追加（未追加なら）

    done = models.BooleanField('完了', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['done', 'deadline', '-updated_at']  # 未完→期限近い順
        
