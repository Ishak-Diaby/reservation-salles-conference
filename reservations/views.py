"""
Views Django pour le système de réservation de salles
Utilise les templates Django au lieu d'une API REST
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from django.http import JsonResponse
from datetime import date, datetime, timedelta

from .models import Utilisateur, Salle, Reservation, Notification, Rapport
from .forms import (
    LoginForm, InscriptionForm, ReservationForm, SalleForm,
    RechercheForm, RapportForm
)


# ==================== AUTHENTIFICATION ====================

def login_view(request):
    """Page de connexion"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenue {user.get_full_name()} !')
                return redirect('dashboard')
            else:
                messages.error(request, 'Identifiants incorrects')
    else:
        form = LoginForm()
    
    return render(request, 'reservations/login.html', {'form': form})


def inscription_view(request):
    """Page d'inscription"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Inscription réussie ! Vous pouvez maintenant vous connecter.')
            return redirect('login')
    else:
        form = InscriptionForm()
    
    return render(request, 'reservations/inscription.html', {'form': form})


@login_required
def logout_view(request):
    """Déconnexion"""
    logout(request)
    messages.info(request, 'Vous êtes déconnecté')
    return redirect('login')


# ==================== DASHBOARD ====================

@login_required
def dashboard(request):
    """Tableau de bord principal"""
    user = request.user
    
    # Statistiques utilisateur
    mes_reservations = Reservation.objects.filter(utilisateur=user)
    total_reservations = mes_reservations.count()
    en_attente = mes_reservations.filter(statut='en_attente').count()
    confirmees = mes_reservations.filter(statut='confirmee').count()
    
    # Prochaines réservations
    today = date.today()
    prochaines = mes_reservations.filter(
        date_reservation__gte=today,
        statut='confirmee'
    ).order_by('date_reservation', 'heure_debut')[:5]
    
    # Notifications non lues
    notifications_count = Notification.objects.filter(
        utilisateur=user,
        est_lue=False
    ).count()
    
    context = {
        'total_reservations': total_reservations,
        'en_attente': en_attente,
        'confirmees': confirmees,
        'prochaines': prochaines,
        'notifications_count': notifications_count,
    }
    
    return render(request, 'reservations/dashboard.html', context)


# ==================== SALLES ====================

@login_required
def liste_salles(request):
    """Liste de toutes les salles"""
    salles = Salle.objects.filter(est_disponible=True).order_by('batiment', 'nom')
    
    # Filtres
    batiment = request.GET.get('batiment')
    type_salle = request.GET.get('type_salle')
    
    if batiment:
        salles = salles.filter(batiment=batiment)
    if type_salle:
        salles = salles.filter(type_salle=type_salle)
    
    # Pour les filtres
    batiments = Salle.objects.values_list('batiment', flat=True).distinct()
    types = Salle.objects.values_list('type_salle', flat=True).distinct()
    
    context = {
        'salles': salles,
        'batiments': batiments,
        'types': types,
    }
    
    return render(request, 'reservations/salles/liste.html', context)


@login_required
def detail_salle(request, pk):
    """Détail d'une salle"""
    salle = get_object_or_404(Salle, pk=pk)
    
    # Réservations de la salle (futures)
    today = date.today()
    reservations = salle.reservations.filter(
        date_reservation__gte=today,
        statut__in=['confirmee', 'en_attente']
    ).order_by('date_reservation', 'heure_debut')
    
    context = {
        'salle': salle,
        'reservations': reservations,
    }
    
    return render(request, 'reservations/salles/detail.html', context)


@login_required
def rechercher_salles(request):
    """Recherche de salles disponibles"""
    form = RechercheForm(request.GET or None)
    salles_disponibles = []
    
    if form.is_valid():
        date_recherche = form.cleaned_data['date_reservation']
        heure_debut = form.cleaned_data['heure_debut']
        heure_fin = form.cleaned_data['heure_fin']
        capacite_min = form.cleaned_data.get('capacite_min')
        type_salle = form.cleaned_data.get('type_salle')
        batiment = form.cleaned_data.get('batiment')
        
        # Rechercher les salles
        salles = Salle.objects.filter(est_disponible=True)
        
        if capacite_min:
            salles = salles.filter(capacite__gte=capacite_min)
        if type_salle:
            salles = salles.filter(type_salle=type_salle)
        if batiment:
            salles = salles.filter(batiment=batiment)
        
        # Vérifier la disponibilité
        for salle in salles:
            if salle.verifier_disponibilite(date_recherche, heure_debut, heure_fin):
                salles_disponibles.append(salle)
    
    context = {
        'form': form,
        'salles': salles_disponibles,
    }
    
    return render(request, 'reservations/salles/recherche.html', context)


# ==================== RÉSERVATIONS ====================

@login_required
def creer_reservation(request, salle_id=None):
    """Créer une nouvelle réservation"""
    salle = None
    if salle_id:
        salle = get_object_or_404(Salle, pk=salle_id)
    
    if request.method == 'POST':
        form = ReservationForm(request.POST, user=request.user, salle=salle)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.utilisateur = request.user
            
            try:
                reservation.save()
                messages.success(
                    request,
                    f'Réservation créée avec succès ! Statut: {reservation.get_statut_display()}'
                )
                return redirect('mes_reservations')
            except Exception as e:
                messages.error(request, f'Erreur: {str(e)}')
    else:
        initial = {}
        if salle:
            initial['salle'] = salle
        form = ReservationForm(initial=initial, user=request.user, salle=salle)
    
    context = {
        'form': form,
        'salle': salle,
    }
    
    return render(request, 'reservations/reservations/creer.html', context)


@login_required
def mes_reservations(request):
    """Liste des réservations de l'utilisateur"""
    statut_filtre = request.GET.get('statut')
    
    reservations = Reservation.objects.filter(
        utilisateur=request.user
    ).select_related('salle').order_by('-date_reservation', '-heure_debut')
    
    if statut_filtre:
        reservations = reservations.filter(statut=statut_filtre)
    
    context = {
        'reservations': reservations,
        'statut_filtre': statut_filtre,
    }
    
    return render(request, 'reservations/reservations/mes_reservations.html', context)


@login_required
def detail_reservation(request, pk):
    """Détail d'une réservation"""
    reservation = get_object_or_404(Reservation, pk=pk)
    
    # Vérifier les droits
    if reservation.utilisateur != request.user and not request.user.is_staff:
        messages.error(request, 'Vous n\'avez pas accès à cette réservation')
        return redirect('mes_reservations')
    
    context = {
        'reservation': reservation,
    }
    
    return render(request, 'reservations/reservations/detail.html', context)


@login_required
def annuler_reservation(request, pk):
    """Annuler une réservation"""
    reservation = get_object_or_404(Reservation, pk=pk)
    
    # Vérifier les droits
    if reservation.utilisateur != request.user and not request.user.is_staff:
        messages.error(request, 'Vous ne pouvez pas annuler cette réservation')
        return redirect('mes_reservations')
    
    # Vérifier le délai
    if not reservation.peut_etre_modifiee():
        messages.error(request, 'Impossible d\'annuler une réservation moins de 2h avant')
        return redirect('detail_reservation', pk=pk)
    
    if request.method == 'POST':
        reservation.annuler()
        messages.success(request, 'Réservation annulée avec succès')
        return redirect('mes_reservations')
    
    context = {
        'reservation': reservation,
    }
    
    return render(request, 'reservations/reservations/annuler.html', context)


# ==================== NOTIFICATIONS ====================

@login_required
def liste_notifications(request):
    """Liste des notifications de l'utilisateur"""
    notifications = Notification.objects.filter(
        utilisateur=request.user
    ).order_by('-created_at')
    
    context = {
        'notifications': notifications,
    }
    
    return render(request, 'reservations/notifications/liste.html', context)


@login_required
def marquer_notification_lue(request, pk):
    """Marquer une notification comme lue"""
    notification = get_object_or_404(Notification, pk=pk, utilisateur=request.user)
    notification.marquer_comme_lue()
    
    return redirect('liste_notifications')


@login_required
def marquer_toutes_lues(request):
    """Marquer toutes les notifications comme lues"""
    Notification.objects.filter(
        utilisateur=request.user,
        est_lue=False
    ).update(est_lue=True)
    
    messages.success(request, 'Toutes les notifications ont été marquées comme lues')
    return redirect('liste_notifications')


# ==================== ADMIN ====================

def est_administrateur(user):
    """Vérifie si l'utilisateur est administrateur"""
    return user.is_staff or user.type_utilisateur == 'administrateur'


@login_required
@user_passes_test(est_administrateur)
def admin_dashboard(request):
    """Dashboard administrateur"""
    # Statistiques globales
    total_reservations = Reservation.objects.count()
    en_attente = Reservation.objects.filter(statut='en_attente').count()
    total_salles = Salle.objects.count()
    total_utilisateurs = Utilisateur.objects.filter(is_active=True).count()
    
    # Réservations en attente
    reservations_attente = Reservation.objects.filter(
        statut='en_attente'
    ).select_related('utilisateur', 'salle').order_by('date_reservation')[:10]
    
    context = {
        'total_reservations': total_reservations,
        'en_attente': en_attente,
        'total_salles': total_salles,
        'total_utilisateurs': total_utilisateurs,
        'reservations_attente': reservations_attente,
    }
    
    return render(request, 'reservations/admin/dashboard.html', context)


@login_required
@user_passes_test(est_administrateur)
def gestion_salles(request):
    """Gestion des salles (admin)"""
    salles = Salle.objects.all().order_by('batiment', 'nom')
    
    context = {
        'salles': salles,
    }
    
    return render(request, 'reservations/admin/salles.html', context)


@login_required
@user_passes_test(est_administrateur)
def creer_salle(request):
    """Créer une nouvelle salle (admin)"""
    if request.method == 'POST':
        form = SalleForm(request.POST)
        if form.is_valid():
            salle = form.save()
            messages.success(request, f'Salle {salle.nom} créée avec succès')
            return redirect('gestion_salles')
    else:
        form = SalleForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'reservations/admin/creer_salle.html', context)


@login_required
@user_passes_test(est_administrateur)
def validation_reservations(request):
    """Validation des réservations en attente (admin)"""
    reservations = Reservation.objects.filter(
        statut='en_attente'
    ).select_related('utilisateur', 'salle').order_by('date_reservation')
    
    context = {
        'reservations': reservations,
    }
    
    return render(request, 'reservations/admin/validation.html', context)


@login_required
@user_passes_test(est_administrateur)
def valider_reservation(request, pk):
    """Valider une réservation (admin)"""
    reservation = get_object_or_404(Reservation, pk=pk)
    
    if request.method == 'POST':
        reservation.valider()
        messages.success(request, 'Réservation validée')
        return redirect('validation_reservations')
    
    return redirect('validation_reservations')


@login_required
@user_passes_test(est_administrateur)
def refuser_reservation(request, pk):
    """Refuser une réservation (admin)"""
    reservation = get_object_or_404(Reservation, pk=pk)
    
    if request.method == 'POST':
        reservation.refuser()
        messages.warning(request, 'Réservation refusée')
        return redirect('validation_reservations')
    
    return redirect('validation_reservations')


@login_required
@user_passes_test(est_administrateur)
def generer_rapport(request):
    """Générer un rapport statistique (admin)"""
    if request.method == 'POST':
        form = RapportForm(request.POST)
        if form.is_valid():
            date_debut = form.cleaned_data['date_debut']
            date_fin = form.cleaned_data['date_fin']
            
            # Calculer les statistiques
            from django.db.models import Count, Sum
            
            reservations = Reservation.objects.filter(
                date_reservation__gte=date_debut,
                date_reservation__lte=date_fin
            )
            
            donnees = {
                'total_reservations': reservations.count(),
                'par_statut': dict(reservations.values('statut').annotate(count=Count('id')).values_list('statut', 'count')),
                'par_type_utilisateur': dict(reservations.values('utilisateur__type_utilisateur').annotate(count=Count('id')).values_list('utilisateur__type_utilisateur', 'count')),
                'salles_populaires': list(reservations.values('salle__nom').annotate(count=Count('id')).order_by('-count')[:10].values_list('salle__nom', 'count')),
            }
            
            # Créer le rapport
            rapport = Rapport.objects.create(
                administrateur=request.user,
                titre=f"Rapport du {date_debut} au {date_fin}",
                type_rapport='utilisation',
                date_debut=date_debut,
                date_fin=date_fin,
                donnees=donnees
            )
            
            messages.success(request, 'Rapport généré avec succès')
            return redirect('detail_rapport', pk=rapport.pk)
    else:
        form = RapportForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'reservations/admin/generer_rapport.html', context)


@login_required
@user_passes_test(est_administrateur)
def detail_rapport(request, pk):
    """Détail d'un rapport (admin)"""
    rapport = get_object_or_404(Rapport, pk=pk)
    
    context = {
        'rapport': rapport,
    }
    
    return render(request, 'reservations/admin/detail_rapport.html', context)