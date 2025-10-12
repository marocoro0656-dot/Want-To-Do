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
        fields = ('title', 'category', 'difficulty', 'deadline')
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }
