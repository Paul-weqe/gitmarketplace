from django import forms

class RegisterUserForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    email = forms.CharField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    first_name = forms.CharField(required=False, widget=forms.TextInput())
    last_name = forms.CharField(required=False, widget=forms.TextInput())


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class CreateRepository(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Repository name'
    }))


class CreateRepositoryFile(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'name': 'Name'
    }))
