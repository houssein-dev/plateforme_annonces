from django.urls import path
from .import views

urlpatterns = [
path('', views.liste_annonces, name='liste_annonces'),  # Liste des annonces
path('ajouter/', views.ajouter_annonce, name='ajouter_annonce'),
path('annonce/<int:annonce_id>/', views.detail_annonce, name='detail_annonce'),
path('derniere_annonce/', views.derniere_annonce, name='derniere_annonce'),
path('annonces_en_attente/', views.annonces_en_attente, name='annonces_en_attente'),
path('recherche/', views.recherche_annonces, name='recherche_annonces'),

path('accueil_vendeur/', views.accueil_vendeur , name="accueil_vendeur"),
path('accueil_visiteurss/', views.accueil_visiteurs , name="accueil_visiteurs"),

path('profil-vendeur/', views.profil_vendeur, name='profil_vendeur'),
path('modifier-vendeur/', views.modifier_profil_vendeur, name='modifier_profil_vendeur'),
]