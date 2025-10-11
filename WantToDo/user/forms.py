import re
from django import forms
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm 
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# パスワードポリシー: 8-24 / 英字1+ / 数字1+ / 記号(!_%@#$&)1+
PASSWORD_RE = re.compile(
    r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[!_%@#$&])[A-Za-z\d!_%@#$&]{8,24}$'
)

def validate_password_policy(pw: str):
    if not PASSWORD_RE.match(pw or ''):
        raise ValidationError(
            'パスワードは8〜24文字、英字・数字・記号(! _ % @ # $ &)を各1文字以上含めてください。'
        )

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 全フィールドにクラスを付与
        for f in self.fields.values():
            f.widget.attrs.update({'class': 'signup-input'})
    """パスワード変更でも独自ポリシーを適用"""
    def clean(self):
        """
        親の clean() を呼ぶことで：
        - 旧パスワードチェック
        - new_password1 / new_password2 の一致チェック
        - settings の AUTH_PASSWORD_VALIDATORS の適用
        を実施。その上で“独自ポリシー”を追加チェック。
        """
        cleaned = super().clean()
        pw2 = cleaned.get('new_password2')
        if pw2:
            validate_password_policy(pw2)
        return cleaned



class SignUpForm(UserCreationForm):
    """
    新規登録: ユーザー名 + メール + パスワード（確認あり）
    """
    email = forms.EmailField(required=True, label='メールアドレス')

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

        # UserCreationForm の標準「一致チェック」を自前で行う
        if pw1 and pw2 and pw1 != pw2:
            raise ValidationError('パスワードが一致しません。')

        # 追加ポリシー
        if pw2:
            validate_password_policy(pw2)

        return pw2

class LoginForm(forms.Form):
    """
    ログイン: メール + パスワード
    """
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(
        label='パスワード', widget=forms.PasswordInput
    )
