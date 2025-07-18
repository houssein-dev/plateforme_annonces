from acceuil.models import Annonce1, Categorie1
from django import forms
from django.forms.widgets import ClearableFileInput


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
        fields = '__all__'
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control', 'id': 'titre', 'required': True}),
            'prix': forms.NumberInput(attrs={'class': 'form-control', 'id': 'prix', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'id': 'description', 'rows': 3, 'required': True}),
            'status': forms.Select(attrs={'class': 'form-control', 'id': 'status'}),
            'categorie': forms.Select(attrs={'class': 'form-control', 'id': 'categorie'}),

        }



