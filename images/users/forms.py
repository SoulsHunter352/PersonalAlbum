from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.core.exceptions import ValidationError


class LoginForm(AuthenticationForm):
    """
    Форма для ввода логина и пароля
    """
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'input'}))

    error_messages = {'invalid_login': 'Неверный логин или пароль, попробуйте заново'}


class RegisterUserForm(UserCreationForm):
    """
    Форма регистрации пользователя
    """
    username = forms.CharField(max_length=50, label='Логин', widget=forms.TextInput(attrs={'class': 'input'}))
    password1 = forms.CharField(max_length=30, label='Пароль', widget=forms.PasswordInput(attrs={'class': 'input'}))
    password2 = forms.CharField(max_length=30, label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'public_email', 'password1', 'password2']
        labels = {
            'email': 'E-mail'
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'input'})
        }

    def clean_username(self):
        """
        Метод для проверки уникальности логина
        :return:
        """
        username = self.cleaned_data['username']
        if get_user_model().objects.filter(username=username).exists():
            raise ValidationError('Данное имя занято')
        return username

    def clean_email(self):
        """
        Метод для проверки наличия аккаунта, зарегистрированного на почту
        :return:
        """
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('На данную почту есть аккаунт')
        return email


class UserChangePasswordForm(PasswordChangeForm):
    """
    Форма для изменения пароля
    """
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='Повторите новый пароль',
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserUpdateForm(forms.ModelForm):
    """
    Форма для обновления данных пользователя
    """
    username = forms.CharField(max_length=50, label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'public_email']
        labels = {'email': 'E-mail'}
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_username(self):
        """
        Проверка на уникальность имени пользователя
        :return:
        """
        username = self.cleaned_data['username']
        if get_user_model().objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise ValidationError('Данное имя пользователя занято')
        return username

    def clean_email(self):
        """
        Проверка на уникальность почты
        :return:
        """
        email = self.cleaned_data['email']
        if get_user_model().objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise ValidationError('На данную почту зарегистрирован аккаунт')
        return email
