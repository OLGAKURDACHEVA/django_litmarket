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
    username = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': True, 'class': 'form-label'}),
        error_messages={
            'required': 'Логин - обязательное поле.',
            'unique': 'Пользователь с таким именем уже существует.',
            'max_length': 'Имя пользователя не должно превышать 150 символов.'
        }
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': True, 'class': 'form-label'}),
        error_messages={
            'required': 'Email - обязательное поле.',
            'invalid': 'Введите корректный адрес электронной почты.'
        }
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-label'}),
        error_messages={
            'required': 'Имя - обязательное поле.',
            'max_length': 'Имя не должно превышать 30 символов.'
        }
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-label'}),
        error_messages={
            'required': 'Фамилия - обязательное поле.',
            'max_length': 'Фамилия не должна превышать 30 символов.'
        }
    )
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-label'}), required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'image')

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name and first_name.strip() == '':
            raise forms.ValidationError('Имя не может состоять только из пробелов.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name and last_name.strip() == '':
            raise forms.ValidationError('Фамилия не может состоять только из пробелов.')
        return last_name