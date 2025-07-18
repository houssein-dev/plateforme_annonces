from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from Dashboard.forms import AnnonceForm
from acceuil.forms import CatagForm
from acceuil.models import Annonce1, Categorie1, ImageAnnonce
from authentification.forms import InscriptionForm
from authentification.models import Utilisateurs

@login_required
def annonces_dash(request):
    if request.user.role != 'admin':
        return redirect('page403')
    annonces_not = Annonce1.objects.filter(status="En attente")
    notifications = []
    
    for annonce in annonces_not:
        notifications.append({
            "titre": annonce.titre,
            "description": annonce.description[:50] + "...",
            "prix": str(annonce.prix) + " MRU",
            
        })
    print(notifications)
    annonces = Annonce1.objects.all()
    if request.method == 'POST':
        form = AnnonceForm(request.POST, request.FILES)
        if form.is_valid():
            annonce = form.save(commit=False) 
           
            annonce.save()
            images = request.FILES.getlist('images')
            print("Images reçues :", images)  

            for image in images:
                ImageAnnonce.objects.create(annonce=annonce, image=image)
            return redirect('annonces_dash')
        
    else:
        form = AnnonceForm()
    return render(request , 'annonces_dash.html',{"annonces":annonces ,'form':form ,'notifications':notifications,"count": len(notifications)})




@login_required
def annonce_detail_dash(request, pk):
    if request.user.role != 'admin':
        return redirect('page403')
    annonces = Annonce1.objects.all()
    annonce = get_object_or_404(Annonce1, pk=pk)
    return render(request, 'detail_annonce_dash.html', {'annonce': annonce})


@login_required
def update_annonce_dash(request, pk):
    if request.user.role != 'admin':
        return redirect('page403')
    annonces = Annonce1.objects.all()
    annonce = get_object_or_404(Annonce1, pk=pk)
    if request.method == 'POST':
        form = AnnonceForm(request.POST, request.FILES, instance=annonce)
        if form.is_valid():
            form.save()
            return redirect('annonces_dash')
        
    else:
        form = AnnonceForm(instance=annonce)
    return render(request , 'annonces_dash.html',{"annonces":annonces ,'form':form})



@login_required
def delete_annonce_dash(request, pk):
    if request.user.role != 'admin':
        return redirect('page403')
    annonce = get_object_or_404(Annonce1, pk=pk)
    if annonce:
        annonce.delete()
        return redirect('annonces_dash')
    
    return render(request, 'annonces_dash.html')


# ====================================================================
#
#       Utilisateur
#
# ======================================================================


@login_required
def update_user_dash(request, pk):
    if request.user.role != 'admin':
        return redirect('page403')
    users = Utilisateurs.objects.all()
    user = get_object_or_404(Utilisateurs, pk=pk)
    if request.method == 'POST':
        form = InscriptionForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('utilisateurs_dash')
    else:
        form = InscriptionForm(instance=user)
    return render(request, 'utilisateurs_dash.html', {'form': form, 'users': users})


@login_required
def delete_user_dash(request, pk):
    if request.user.role != 'admin':
        return redirect('page403')
    user = get_object_or_404(Utilisateurs, pk=pk)
    if user:
            user.delete()
            return redirect('utilisateurs_dash')
    return render(request , 'utilisateurs_dash.html')


@login_required
def user_detail_dash(request, pk):
    if request.user.role != 'admin':
        return redirect('page403')
    
    vendeur = get_object_or_404(Utilisateurs, pk=pk)
    annonces = Annonce1.objects.filter(auteur=vendeur.id)  # Récupérer les annonces du vendeur

    return render(request, 'user_detail_dash.html', {'vendeur': vendeur, 'annonces': annonces})

@login_required
def utilisateurs_dash(request):
    if request.user.role != 'admin':
        return redirect('page403')
    users = Utilisateurs.objects.all()
    if request.method == 'POST':
        form = InscriptionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('utilisateurs_dash')
        pass
    else:
        form  = InscriptionForm()
    return render(request , 'utilisateurs_dash.html',{'users':users ,'form': form})



@login_required
def profil_vendeur(request):
    if request.user.role != 'admin':
        return redirect('page403')
    
    vendeur = request.user  # Récupérer l'utilisateur connecté
    annonces = Annonce1.objects.filter(publier_par=vendeur.id)  # Récupérer les annonces du vendeur
    print(vendeur)
    return render(request, 'profile_vendeur.html', {'vendeur': vendeur, 'annonces': annonces})


# =====================================================================
# =====================================================================
#       catagories
# ======================================================================
# ======================================================================

@login_required
def catagories_dash(request):
    if request.user.role != 'admin':
        return redirect('page403')
    catags = Categorie1.objects.all()
    if request.method == 'POST':
        form = CatagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('catagories_dash')
    else:
        form = CatagForm()
    return render(request , 'catagories_dash.html',{'catagos' : catags,'form':form})



@login_required
def update_catag_dash(request, pk):
    if request.user.role != 'admin':
        return redirect('page403')
    catags = Categorie1.objects.all()
    catag = get_object_or_404(Categorie1, id=pk)
    if request.method == 'POST':
        form = CatagForm(request.POST, request.FILES, instance=catag)
        if form.is_valid():
            form.save()
            return redirect('catagories_dash')
    else:
        form = CatagForm(instance=catag)
        print(catags)
    return render(request, 'catagories_dash.html', {'form': form, 'catagos': catags})



@login_required
def delete_catag_dash(request, pk):
    if request.user.role != 'admin':
        return redirect('page403')
    
    catag = get_object_or_404(Categorie1, id=pk)
    if catag:
            catag.delete()
            return redirect('catagories_dash')
    return render(request , 'catagories_dash.html')




@login_required
def notification_annonce(request):
    if request.user.role != 'admin':
        return redirect('page403')
    
    annonces_not = Annonce1.objects.filter(status="En attente").order_by("-date_publication")[:]
    notifications = []
    
    for annonce in annonces_not:
        notifications.append({
            "titre": annonce.titre,
            "description": annonce.description[:50] + "...",
            "prix": str(annonce.prix) + " MRU",
            "date": annonce.date_publication.strftime("%d/%m/%Y"),
           
        })
    print(notifications)
    render(request , 'topbar.html',{"notifications":notifications, "count": len(notifications) })



from django.shortcuts import render

def get_403(request):
        
        return render(request, 'page_403.html', status=403)  
    



