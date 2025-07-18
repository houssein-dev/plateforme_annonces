from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Utilisateurs

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Utilisateurs

class InscriptionForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        max_length=75,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre email'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom d\'utilisateur'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmez le mot de passe'})
    )
    nom = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lastname'})
    )
    prenom = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Firstname'})
    )
    phone = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Numero telephone'})
    )
   

    class Meta:
        model = Utilisateurs
        fields = ["username", "email", "nom", "prenom", "phone", "password1", "password2"]


class ConnexionForm(AuthenticationForm):
    username = forms.CharField(
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': "Nom d'utilisateur"})
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Mot de passe'})
    )

class ProfilVendeurForm(forms.ModelForm):
    class Meta:
        model = Utilisateurs
        fields = ['nom', 'prenom', 'username', 'email', 'phone', 'profile_photo']