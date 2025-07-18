from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from acceuil.forms import AnnonceForm
from acceuil.models import Annonce1, ImageAnnonce
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from authentification.forms import ProfilVendeurForm

# Create your views here.
# @login_required
def liste_annonces(request):
    annonces = Annonce1.objects.filter(status='Validee').order_by('-date_publication')
    paginator = Paginator(annonces, 6)  # 6 annonces par page
    page = request.GET.get('page')
    annonces = paginator.get_page(page)
    return render(request, 'acceuil/dashboard.html', {'annonces': annonces})

@login_required
def ajouter_annonce(request):
    base_template = './acceuil/vendeur/base_vend.html' if request.user.is_authenticated else 'base.html'

    if request.method == "POST":
        form = AnnonceForm(request.POST, request.FILES)
        if form.is_valid():
            annonce = form.save(commit=False)  # On empêche la sauvegarde immédiate
            annonce.auteur = request.user  # Associe l'annonce à l'utilisateur connecté
            annonce.save()
            images = request.FILES.getlist('images')
            print("Images reçues :", images)  # Debugging

            # Enregistrer chaque image avec l'annonce
            for image in images:
                ImageAnnonce.objects.create(annonce=annonce, image=image)

            return redirect('accueil_vendeur')  # Redirection après ajout
    else:
        form = AnnonceForm()

    return render(request, 'acceuil/ajouter_annonce.html', {'form': form, 'base_template':base_template})

def detail_annonce(request, annonce_id):
    annonce = get_object_or_404(Annonce1, id=annonce_id)
    base_template = './acceuil/vendeur/base_vend.html' if request.user.is_authenticated else 'base.html'

    return render(request, 'acceuil/detail_annonce.html', {'annonce': annonce , 'base_template':base_template})


def derniere_annonce(request):
    annonces = Annonce1.objects.filter(status="En attente").order_by("-date_publication")[:5]
    data = []
    
    for annonce in annonces:
        data.append({
            "titre": annonce.titre,
            "description": annonce.description[:50] + "...",
            "prix": str(annonce.prix) + " €",
            "date": annonce.date_publication.strftime("%d/%m/%Y"),
            "url": f"/annonce/{annonce.id}/"
        })
    
    return JsonResponse({"annonces": data, "count": len(data)})

def annonces_en_attente(request):
    nb_annonces = Annonce1.objects.filter(status="En attente").count()
    return JsonResponse({"count": nb_annonces})


from django.shortcuts import render
from acceuil.models import Annonce1, Categorie1

def recherche_annonces(request):
    query = request.GET.get('q', '').strip()  # Récupérer le terme de recherche
    annonces = []

    if query:
        # Recherche dans les titres d'annonces
        annonces_par_titre = Annonce1.objects.filter(titre__icontains=query, status='Validee')

        # Recherche par nom de catégorie
        categories = Categorie1.objects.filter(nom__icontains=query)
        annonces_par_categorie = Annonce1.objects.filter(categorie__in=categories, status='Validee')

        # Fusionner les résultats sans doublons
        annonces = (annonces_par_titre | annonces_par_categorie).distinct()

    return render(request, 'acceuil/recherche_annonces.html', {'annonces': annonces, 'query': query})

@login_required
def accueil_vendeur(request):
    annonces = Annonce1.objects.filter(status='Validee').order_by('-date_publication')
    paginator = Paginator(annonces, 6)  # 6 annonces par page
    page = request.GET.get('page')
    annonces = paginator.get_page(page)
    
    return render(request , 'acceuil/vendeur/acceuil.html', {'annonces': annonces})

def accueil_visiteurs(request):
    
    return render(request , 'visiteur/accueil.html')


@login_required
def profil_vendeur(request):
    vendeur = request.user  # Récupérer l'utilisateur connecté
    annonces = Annonce1.objects.filter(auteur=vendeur.id)  # Récupérer les annonces du vendeur

    return render(request, 'acceuil/vendeur/profile_vendeur.html', {'vendeur': vendeur, 'annonces': annonces})


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
