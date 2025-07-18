from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class Utilisateurs(AbstractUser):
    ROLE_CHOICES = [
    ("vandeur", "vandeur"),
    ("admin", "admin"),
   
    ]
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=75)
    role = models.CharField(choices=ROLE_CHOICES,max_length=10, null=True, default="vandeur")
    profile_photo = models.ImageField(upload_to='profile_photos/', default='profile_photos/default.jpg')
    phone = models.CharField(max_length=8)



    # # Correction des conflits avec auth.User
    # groups = models.ManyToManyField(Group, related_name="custom_user_set")
    # user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions_set")

    def __str__(self):
        return f"{self.username}  {self.role if self.role else ''}"
