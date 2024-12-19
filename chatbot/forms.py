from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="아이디",
        max_length=150,
        help_text="150자 이하 문자, 숫자 그리고 @/./+/-/_ 만 가능합니다.",
        widget=forms.TextInput(attrs={"placeholder": "아이디를 입력하세요"})
    )
    password1 = forms.CharField(
        label="비밀번호",
        help_text="비밀번호는 8자 이상이어야 하며, 숫자로만 구성될 수 없습니다.",
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호를 입력하세요"})
    )
    password2 = forms.CharField(
        label="비밀번호 확인",
        help_text="비밀번호를 다시 입력해 주세요.",
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호를 다시 입력하세요"})
    )

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
        labels = {
            "username": "아이디",
        }
