# acceuil/forms.py
from django import forms
from django.forms.widgets import ClearableFileInput
from .models import Annonce1, Categorie1, ImageAnnonce

# ── STEP 1 ── Créer un widget « multi‑fichiers »
class MultiFileInput(ClearableFileInput):
    allow_multiple_selected = True  # ← autorise le multiple

# ── STEP 2 ── Utiliser ce widget dans le formulaire
class AnnonceForm(forms.ModelForm):
    images = forms.FileField(
        widget=MultiFileInput(attrs={'multiple': True}),
        required=False
    )

    class Meta:
        model = Annonce1
        fields = ['titre', 'description', 'prix', 'categorie']

class CatagForm(forms.ModelForm):
    class Meta:
        model = Categorie1
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'titre',
                'required': True
            }),
        }
