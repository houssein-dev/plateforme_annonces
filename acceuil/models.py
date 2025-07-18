from django.db import models
from authentification.models import Utilisateurs

class Categorie1(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Annonce1(models.Model):
    STATUS_CHOICES = [
    ("En attente", "En attente"),
    ("Validee", "Validee"),
    ("Rejetee", "Rejetee"),
    ]
    titre = models.CharField(max_length=200)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    date_publication = models.DateTimeField(auto_now_add=True)
    auteur = models.ForeignKey(Utilisateurs, on_delete=models.SET_NULL, null=True, blank=True)
    categorie = models.ForeignKey(Categorie1, on_delete=models.SET_NULL, null=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=16, default= 'En attente')

    def __str__(self):
        return self.titre


class ImageAnnonce(models.Model):
    annonce = models.ForeignKey(Annonce1, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='annonces/')

    def __str__(self):
        return f"Image de {self.annonce.titre}"