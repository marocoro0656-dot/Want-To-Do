import re
from django import forms
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# パスワードポリシー: 8-24 / 英字1+ / 数字1+ / 記号(!_%@#$&)1+
PASSWORD_RE = re.compile(
    r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[!_%@#$&])[A-Za-z\d!_%@#$&]{8,32}$'
)

def validate_password_policy(pw: str):
    if not PASSWORD_RE.match(pw or ''):
        raise ValidationError(
            'パスワードは半角英数字含む8文字以上、記号(! _ % @ # $ &)を1文字以上含めてください。'
        )

#パスワード変更
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 全フィールドにクラスを付与
        for f in self.fields.values():
            f.widget.attrs.update({'class': 'signup-input'})

    def clean_new_password1(self):
        new_password1 = self.cleaned_data.get('new_password1')
        old_password = self.cleaned_data.get('old_password')

        # 新旧が同じ場合にエラー
        if new_password1 and old_password and new_password1 == old_password:
            raise ValidationError("現在のパスワードと同じです。別のパスワードを設定してください。")

        return new_password1

    def clean(self):
        cleaned_data = super().clean()
        new_password2 = cleaned_data.get('new_password2')
        if new_password2:
            validate_password_policy(new_password2)
        return cleaned_data




class SignUpForm(UserCreationForm):
    """
    新規登録: ユーザー名 + メール + パスワード（確認あり）
    """
    username = forms.CharField(
        label='ユーザー名',
        max_length=32,
        required=True,
    )
    email = forms.EmailField(
        label='メールアドレス',
        max_length=128,
        required=True,
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('このメールアドレスは既に使用されています。')
        return email

    def clean_password2(self):
        pw1 = self.cleaned_data.get('password1')
        pw2 = self.cleaned_data.get('password2')

        # 一致チェック
        if pw1 and pw2 and pw1 != pw2:
            raise ValidationError('パスワードが一致しません。')

        # 追加ポリシー
        if pw2:
            validate_password_policy(pw2)

        return pw2

#ログイン
class LoginForm(forms.Form):
    """
    ログイン: メール + パスワード
    """
    email = forms.EmailField(
        label='メールアドレス',
        required=True,
        error_messages={
            'required': 'メールアドレスを入力してください。',
            'invalid': '正しいメールアドレスの形式で入力してください。',
        },
        widget=forms.EmailInput(attrs={'class': 'signup-input'})
    )
    password = forms.CharField(
        label='パスワード',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'signup-input'}),
        error_messages={
            'required': 'パスワードを入力してください。',
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        # 両方未入力などのときに、明確にエラーを出す
        if not email or not password:
            raise forms.ValidationError("メールアドレスとパスワードを入力してください。")

        return cleaned_data

#メールアドレス変更
class EmailChangeForm(forms.Form):
    email = forms.EmailField(label='新しいメールアドレス')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # request.user を受け取る
        super().__init__(*args, **kwargs)

    def clean_email(self):
        new_email = self.cleaned_data['email']
        if self.user and new_email == self.user.email:
            raise ValidationError("現在のメールアドレスと同じです。別のメールアドレスを入力してください。")
        return new_email

