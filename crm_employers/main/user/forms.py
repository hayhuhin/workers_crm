from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField
from django.contrib.auth.models import User
from django import forms


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('username','email','password1','password2')


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):    
        super(UserLoginForm, self).__init__(*args, **kwargs)

        username = UsernameField(widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '', 'id': 'hello'}))
        password = forms.CharField(widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '',
                'id': 'hi',
            }
    ))