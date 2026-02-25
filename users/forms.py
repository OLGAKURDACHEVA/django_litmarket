from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from users.models import User
from django import forms

class UserLoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input',
        'placeholder': 'Введите имя пользователя',
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input',
        'placeholder': 'Введите пароль',
    }))


    class Meta:
        model = User
        fields = ('username', 'password')

class UserRegisterForm(UserCreationForm):

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Введите имя',

        })
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Введите фамилию',

        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Введите адрес эл. почты',

        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Введите имя пользователя',

        })
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Введите пароль',

        })
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Подтвердите пароль',

        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class UserProfileForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly': True, 'class': 'form-label'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'readonly': True, 'class': 'form-label'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-label'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-label'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-label'}), required=False)


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'image')