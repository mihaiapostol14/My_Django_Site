from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm
)
from django.forms import ModelForm

User = get_user_model()


class RegistrationUserForm(ModelForm): # README: RegistrationUserForm 👈 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.label_suffix = ''

        self.fields['first_name'].widget.attrs.update({
            'required': '',
            'type': 'text',
            'name': 'first_name',
            'id': 'first_name',
            'class': 'form-control',
            'placeholder': 'Peter',
            'value': '',
            'maxlength': '50',
            'minlength': '4'
        }),

        self.fields['last_name'].widget.attrs.update({
            'required': '',
            'type': 'text',
            'name': 'last_name',
            'id': 'last_name',
            'class': 'form-control',
            'placeholder': 'Parker',
            'value': '',
            'maxlength': '50',
            'minlength': '4'
        }),

        self.fields['email'].widget.attrs.update({
            'required': '',
            'type': 'email',
            'name': 'email',
            'id': 'email',
            'class': 'form-control',
            'placeholder': 'PiterParker@gmail.com',
            'value': ''
        })

        self.fields['password'].widget.attrs.update({
            'required': '',
            'type': 'password',
            'name': 'password',
            'id': 'password',
            'class': 'form-control',
            'placeholder': 'PiterParker1234',
            'value': '',
            'maxlength': '8',
            'minlength': '5'
        })

        self.fields['photo'].widget.attrs.update({
            'type': 'file',
            'name': 'photo',
            'id': 'photo',
            'class': 'form-control',
            'maxlength': '8',

        })

    class Meta:
        model = User
        fields = ['first_name','last_name', 'email', 'password', 'photo']
        labels = {
            'username': 'Username',
            'email': 'Email Address',
            'password': "Password",
            'photo': 'Upload Your Photo',
        }

        widgets = {
            'password': forms.PasswordInput(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user



class LoginUserForm(AuthenticationForm): # README: LoginUserForm 👈
    username = forms.EmailField(
        label="Email",
        widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': True})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class ChangeUserPasswordForm(PasswordChangeForm): # README: ChangeUserPasswordForm 👈
    new_password1 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']
