from django.contrib.auth import get_user_model
from django.forms import CharField, EmailField, PasswordInput, ValidationError
from django.forms import Form

User = get_user_model()


class UserRegisterForm(Form):
    username = CharField()
    email = EmailField()
    password = CharField(widget=PasswordInput)
    password_confirm = CharField(widget=PasswordInput, label='Confirm Password')

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise ValidationError("Check that passwords are spelled correctly.")
        return password_confirm

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__icontains=username).exists():
            raise ValidationError("This username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__icontains=email).exists():
            raise ValidationError("This email is already registered.")
        return email