from django import forms
from .models import Want

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

class FilterForm(forms.Form):
    CATEGORY_BLANK = [('', '選択しない')]
    DIFFICULTY_BLANK = [('', '選択しない')]

    category = forms.ChoiceField(
        choices=CATEGORY_BLANK + Want.CATEGORY_CHOICES,
        required=False, label='カテゴリ',
        widget=forms.Select(attrs={'class': 'filter-select'})
    )
    difficulty = forms.ChoiceField(
        choices=DIFFICULTY_BLANK + Want.DIFFICULTY_CHOICES,
        required=False, label='難易度',
        widget=forms.Select(attrs={'class': 'filter-select'})
    )
    start_date = forms.DateField(
        required=False, label='開始日',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'filter-date'})
    )
    end_date = forms.DateField(
        required=False, label='終了日',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'filter-date'})
    )


class WantForm(forms.ModelForm):
    class Meta:
        model = Want
        fields = ('title', 'deadline', 'category', 'difficulty', 'memo')
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            # memo は CharField だがテキストエリアで入力したいので後で __init__ で差し替える
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 必須設定（モデルは blank=True だがフォームでは必須にする）
        self.fields['title'].required = True
        self.fields['category'].required = True
        self.fields['difficulty'].required = True
        self.fields['deadline'].required = False   # 任意

        # メモ：テキストエリアに差し替え（120文字）
        self.fields['memo'].required = False
        self.fields['memo'].widget = forms.Textarea(attrs={
            'rows': 3,
            'maxlength': 120,
            'placeholder': '120文字以内でメモを残せます'
        })

        # 全フィールドに共通の見た目クラスを付与（中央寄せスタイルと統一）
        for name, f in self.fields.items():
            base = f.widget.attrs.get('class', '')
            f.widget.attrs['class'] = (base + ' signup-input').strip()
            # プレースホルダも少し気持ちよく
            if name == 'title':
                f.widget.attrs.setdefault('placeholder', 'タイトルを入力')

    def clean(self):
        cleaned = super().clean()
        # 追加の整合チェックがあればここに（今は不要）
        return cleaned

    def error_messages_for(self, field_name):
        """テンプレで楽に使える小ヘルパ（任意）"""
        return self[field_name].errors
