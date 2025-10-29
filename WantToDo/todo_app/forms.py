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
        widget=forms.Select(attrs={'class': 'filter-select',})
    )
    difficulty = forms.ChoiceField(
        choices=CATEGORY_BLANK + Want.DIFFICULTY_CHOICES,
        required=False, label='難易度',
        widget=forms.Select(attrs={'class': 'filter-select',})
    )
    start_date = forms.DateField(
        required=False, label='開始日',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'filter-date'})
    )
    end_date = forms.DateField(
        required=False, label='終了日',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'filter-date'})
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError('終了日は開始日以降の日付を選択してください。')

        return cleaned_data


class WantForm(forms.ModelForm):
    class Meta:
        model = Want
        fields = ('title', 'deadline', 'category', 'difficulty', 'memo')
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].required = True
        self.fields['category'].required = True
        self.fields['difficulty'].required = True
        self.fields['deadline'].required = False   # 任意
        self.fields['memo'].required = False

        self.fields['memo'].widget = forms.Textarea(attrs={
            'rows': 6,
            'maxlength': 120,
            'placeholder': '120文字以内でメモを残せます'
        })

        self.fields['title'].widget.attrs.update({
            'placeholder': 'タイトルを入力',
            'maxlength': 64,
        })


        for name, f in self.fields.items():
            base = f.widget.attrs.get('class', '')
            f.widget.attrs['class'] = (base + ' signup-input').strip()
            if name == 'title':
                f.widget.attrs.setdefault('placeholder', 'タイトルを入力')

    # --- タイトル文字数チェック（65文字以上でエラー） ---
    def clean_title(self):
        title = self.cleaned_data.get('title', '')
        if len(title) > 64:
            raise forms.ValidationError('タイトルは64文字以内で入力してください。')
        return title

    # --- メモ文字数チェック（121文字以上でエラー） ---
    def clean_memo(self):
        memo = self.cleaned_data.get('memo', '')
        if len(memo) > 120:
            raise forms.ValidationError('メモは120文字以内で入力してください。')
        return memo

    def clean(self):
        cleaned = super().clean()
        return cleaned

    def error_messages_for(self, field_name):
        return self[field_name].errors
