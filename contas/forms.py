from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# class UserRegisterForm(UserCreationForm):
#     email = forms.EmailField(required=True)

#     class Meta:
#         model = User
#         fields = ["username", "email", "password1", "password2"]
    
#     def save(self, commit=True):
#         user = super().save(commit=False)

#         # user.username = self.cleaned_data["username"]
#         user.email = self.cleaned_data["email"]
#         # user.set_password(self.cleaned_data["password1"])

#         if commit:
#             user.save()
#         return user
    
    
#     def clean_email(self):
#         """Valida se o email está em branco ou já existe no banco."""
#         email = self.cleaned_data.get("email")

#         if not email:
#             raise forms.ValidationError("Selecione um código válido.")

#         # verifica se já existe alguma ação com esse código
#         if  User.objects.filter(email=email).exists():
#             raise forms.ValidationError(f"O '{email}' já está cadastrado.")

#         return email

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "nome")
