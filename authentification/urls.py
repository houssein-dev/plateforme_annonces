
from django.urls import path
from django.conf.urls.static import static
from annonces_esp import settings
from . import views
from .views import *
urlpatterns = [
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
   
    path('profil-vendeur/', views.profil_vendeur, name='profil_vendeur'),
    path('modifier-vendeur/', views.modifier_profil_vendeur, name='modifier_profil_vendeur'),
    path('password-reset/', password_reset, name='password_reset'),
    path('password-reset/<uidb64>/<token>/', password_reset, name='password_reset_confirm'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)