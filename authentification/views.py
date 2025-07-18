from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from acceuil.models import Annonce1
from .forms import InscriptionForm, ProfilVendeurForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import ConnexionForm


from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from django.contrib.auth import get_user_model

def password_reset(request, uidb64=None, token=None):
    User = get_user_model()

    if uidb64 and token:
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            if request.method == "POST":
                form = SetPasswordForm(user, request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Votre mot de passe a été réinitialisé avec succès !")
                    return redirect("connexion")
                else:
                    messages.error(request, "Une erreur s'est produite. Vérifiez vos informations.")  

            else:
                form = SetPasswordForm(user)

            return render(request, "password_reset.html", {"form": form, "validlink": True})

        else:
            messages.error(request, "Lien invalide ou expiré.")
            return redirect("password_reset")

    else:
        if request.method == "POST":
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data["email"]
                users = User.objects.filter(email=email)

                if users.exists():
                    for user in users:
                        uid = urlsafe_base64_encode(force_bytes(user.pk))
                        token = default_token_generator.make_token(user)
                        reset_url = f"{settings.SITE_URL}/auth/password-reset/{uid}/{token}/"

                        subject = "Réinitialisation de votre mot de passe"
                        message = render_to_string("password_reset_email.txt", {"reset_url": reset_url, "user": user})

                        try:
                            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)
                            messages.success(request, "Un email a été envoyé avec un lien de réinitialisation.")
                            return redirect("connexion")
                        except Exception as e:
                            messages.error(request, f"Erreur lors de l'envoi de l'email : {e}")

                else:
                    messages.error(request, "Aucun compte trouvé avec cet email.")

        else:
            form = PasswordResetForm()

        return render(request, "password_reset.html", {"form": form, "validlink": False})




def inscription(request):
    if request.method == "POST":
        form = InscriptionForm(request.POST)
        if form.is_valid():
            form.save()  # Enregistre l'utilisateur
            return redirect('connexion')  # Redirige après l'inscription
    else:
        form = InscriptionForm()

    return render(request, 'inscription.html', {'form': form})




def connexion(request):
    if request.method == 'POST':
       form = ConnexionForm(redirect, data=request.POST)
       if form.is_valid():
           user = form.get_user()
           login(request, user)
           if user.role == 'admin':
              next_url = request.GET.get('next', '/dashboard/')
              return redirect(next_url)
           else:
                next_url = request.GET.get('next', '/accueil_vendeur/')
                return redirect(next_url)
       else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = ConnexionForm()
    return render(request, 'connexion.html', {'form': form})



def est_admin(user):
    return user.role and user.role.nom == "admin"

def est_vendeur(user):
    return user.role and user.role.nom == "vendeur"







@login_required
def deconnexion(request):
    logout(request)
    return redirect('liste_annonces')


@login_required
def profil_vendeur(request):
    vendeur = request.user  # Récupérer l'utilisateur connecté
    annonces = Annonce1.objects.filter(auteur=vendeur.id)  # Récupérer les annonces du vendeur

    return render(request, 'profile_vendeur.html', {'vendeur': vendeur, 'annonces': annonces})


@login_required
def modifier_profil_vendeur(request):
    vendeur = request.user
    if request.method == "POST":
        form = ProfilVendeurForm(request.POST, request.FILES, instance=vendeur)
        if form.is_valid():
            form.save()
            return redirect('profil_vendeur')
    else:
        form = ProfilVendeurForm(instance=vendeur)

    return render(request, 'modifier_profil_vendeur.html', {'form': form})

