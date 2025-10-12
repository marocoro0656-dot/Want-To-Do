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
    category = models.CharField('カテゴリ', max_length=20, choices=CATEGORY_CHOICES, blank=True)
    difficulty = models.CharField('難易度', max_length=10, choices=DIFFICULTY_CHOICES, blank=True)
    deadline = models.DateField('期限', null=True, blank=True)
    done = models.BooleanField('完了', default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['done', 'deadline', '-updated_at']  # 既定の並び（未完→期限近い順）
        indexes = [
            models.Index(fields=['user', 'done', 'deadline']),
        ]

    def __str__(self):
        return f'{self.title} ({self.get_category_display() or "-"})'
