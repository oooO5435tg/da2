from django import forms
from django.core.exceptions import ValidationError
from .models import User
from .models import user_registrated
from django.contrib.auth.forms import AuthenticationForm


class RegisterUserForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput, )
    password2 = forms.CharField(label='Пароль (повторно)', widget=forms.PasswordInput, help_text='Повторите тот же самый пароль еще раз')

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError(
                'Введенные пароли не совпадают', code='password_mismatch'
            )}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=True)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = True
        if commit:
            user.save()
        user_registrated.send(RegisterUserForm, instance=user)
        return user

    class Meta:
        model = User
        fields = ('username', 'avatar')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Введите логин', widget=forms.TextInput)
    password = forms.CharField(label='Введите пароль', widget=forms.PasswordInput)
