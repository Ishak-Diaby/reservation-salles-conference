"""
Modèles Django pour le système de réservation de salles
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Q
from datetime import datetime, timedelta, date


class Utilisateur(AbstractUser):
    """
    Modèle utilisateur personnalisé étendant AbstractUser
    Gère les étudiants, professeurs et administrateurs
    """
    TYPE_CHOICES = [
        ('etudiant', 'Étudiant'),
        ('professeur', 'Professeur'),
        ('administrateur', 'Administrateur'),
    ]
    
    NIVEAU_CHOICES = [
        ('L1', 'Licence 1'),
        ('L2', 'Licence 2'),
        ('L3', 'Licence 3'),
        ('M1', 'Master 1'),
        ('M2', 'Master 2'),
    ]
    
    type_utilisateur = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='etudiant',
        verbose_name="Type d'utilisateur"
    )
    
    niveau = models.CharField(
        max_length=10,
        choices=NIVEAU_CHOICES,
        blank=True,
        null=True,
        verbose_name="Niveau d'études",
        help_text="Pour les étudiants uniquement"
    )
    
    departement = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Département",
        help_text="Pour les professeurs uniquement"
    )
    
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_type_utilisateur_display()})"
    
    def clean(self):
        """Validation personnalisée"""
        super().clean()
        
        if self.type_utilisateur == 'etudiant' and not self.niveau:
            raise ValidationError({
                'niveau': 'Le niveau est requis pour les étudiants'
            })
        
        if self.type_utilisateur == 'professeur' and not self.departement:
            raise ValidationError({
                'departement': 'Le département est requis pour les professeurs'
            })


class Salle(models.Model):
    """
    Modèle représentant une salle de conférence
    """
    TYPE_CHOICES = [
        ('amphi', 'Amphithéâtre'),
        ('td', 'Salle de TD'),
        ('tp', 'Salle de TP'),
        ('conference', 'Salle de conférence'),
        ('reunion', 'Salle de réunion'),
    ]
    
    nom = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nom de la salle"
    )
    
    batiment = models.CharField(
        max_length=100,
        verbose_name="Bâtiment"
    )
    
    etage = models.IntegerField(
        default=0,
        verbose_name="Étage"
    )
    
    capacite = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Capacité",
        help_text="Nombre maximum de personnes"
    )
    
    type_salle = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name="Type de salle"
    )
    
    equipements = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Équipements",
        help_text="Liste des équipements disponibles"
    )
    
    est_disponible = models.BooleanField(
        default=True,
        verbose_name="Est disponible"
    )
    
    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Dernière modification"
    )
    
    class Meta:
        verbose_name = "Salle"
        verbose_name_plural = "Salles"
        ordering = ['batiment', 'nom']
        indexes = [
            models.Index(fields=['batiment', 'type_salle']),
            models.Index(fields=['est_disponible']),
        ]
    
    def __str__(self):
        return f"{self.nom} ({self.batiment})"
    
    def verifier_disponibilite(self, date_reservation, heure_debut, heure_fin, reservation_id=None):
        """
        Vérifie si la salle est disponible pour un créneau donné
        
        Args:
            date_reservation: Date de la réservation
            heure_debut: Heure de début
            heure_fin: Heure de fin
            reservation_id: ID de la réservation à exclure (pour modification)
        
        Returns:
            bool: True si disponible, False sinon
        """
        if not self.est_disponible:
            return False
        
        # Construire la requête de conflit
        conflits = self.reservations.filter(
            date_reservation=date_reservation,
            statut__in=['en_attente', 'confirmee']
        ).filter(
            Q(heure_debut__lt=heure_fin, heure_fin__gt=heure_debut)
        )
        
        # Exclure la réservation en cours de modification
        if reservation_id:
            conflits = conflits.exclude(id=reservation_id)
        
        return not conflits.exists()


class Reservation(models.Model):
    """
    Modèle représentant une réservation de salle
    """
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirmee', 'Confirmée'),
        ('annulee', 'Annulée'),
        ('refusee', 'Refusée'),
    ]
    
    utilisateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='reservations',
        verbose_name="Utilisateur"
    )
    
    salle = models.ForeignKey(
        Salle,
        on_delete=models.CASCADE,
        related_name='reservations',
        verbose_name="Salle"
    )
    
    date_reservation = models.DateField(
        verbose_name="Date de réservation"
    )
    
    heure_debut = models.TimeField(
        verbose_name="Heure de début"
    )
    
    heure_fin = models.TimeField(
        verbose_name="Heure de fin"
    )
    
    motif = models.TextField(
        verbose_name="Motif",
        help_text="Raison de la réservation"
    )
    
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='en_attente',
        verbose_name="Statut"
    )
    
    nombre_participants = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Nombre de participants"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Dernière modification"
    )
    
    class Meta:
        verbose_name = "Réservation"
        verbose_name_plural = "Réservations"
        ordering = ['-date_reservation', '-heure_debut']
        indexes = [
            models.Index(fields=['date_reservation', 'statut']),
            models.Index(fields=['utilisateur', 'statut']),
            models.Index(fields=['salle', 'date_reservation']),
        ]
    
    def __str__(self):
        return f"{self.salle.nom} - {self.date_reservation} à {self.heure_debut}"
    
    def clean(self):
        """Validation personnalisée"""
        super().clean()
        
        # Vérifier que la date n'est pas dans le passé
        if self.date_reservation and self.date_reservation < date.today():
            raise ValidationError({
                'date_reservation': "La date ne peut pas être dans le passé"
            })
        
        # Vérifier que heure_fin > heure_debut
        if self.heure_debut and self.heure_fin and self.heure_fin <= self.heure_debut:
            raise ValidationError({
                'heure_fin': "L'heure de fin doit être après l'heure de début"
            })
        
        # Calculer et vérifier la durée
        if self.heure_debut and self.heure_fin:
            debut = datetime.combine(date.today(), self.heure_debut)
            fin = datetime.combine(date.today(), self.heure_fin)
            duree = (fin - debut).total_seconds() / 60
            
            if duree < 30:
                raise ValidationError("Durée minimale : 30 minutes")
            
            if duree > 240:
                raise ValidationError("Durée maximale : 4 heures")
        
        # Vérifier la capacité
        if self.salle and self.nombre_participants:
            if self.nombre_participants > self.salle.capacite:
                raise ValidationError({
                    'nombre_participants': f"La salle a une capacité de {self.salle.capacite} personnes"
                })
        
        # Vérifier la disponibilité
        if all([self.salle, self.date_reservation, self.heure_debut, self.heure_fin]):
            if not self.salle.verifier_disponibilite(
                self.date_reservation,
                self.heure_debut,
                self.heure_fin,
                self.pk
            ):
                raise ValidationError("La salle n'est pas disponible pour ce créneau")
    
    def peut_etre_modifiee(self):
        """Vérifie si la réservation peut être modifiée (>2h avant)"""
        if not self.date_reservation or not self.heure_debut:
            return False
        
        debut_reservation = datetime.combine(
            self.date_reservation,
            self.heure_debut
        )
        debut_reservation = timezone.make_aware(debut_reservation)
        
        return debut_reservation - timezone.now() > timedelta(hours=2)
    
    def valider(self):
        """Valide la réservation"""
        self.statut = 'confirmee'
        self.save()
    
    def annuler(self):
        """Annule la réservation"""
        self.statut = 'annulee'
        self.save()
    
    def refuser(self):
        """Refuse la réservation"""
        self.statut = 'refusee'
        self.save()
    
    def save(self, *args, **kwargs):
        """Override save pour déterminer le statut initial"""
        # Si c'est une nouvelle réservation
        if not self.pk and not kwargs.get('force_insert', False):
            # Déterminer le statut selon le type d'utilisateur
            if self.utilisateur.type_utilisateur in ['professeur', 'administrateur']:
                self.statut = 'confirmee'
            else:
                self.statut = 'en_attente'
        
        # Validation complète
        self.full_clean()
        
        super().save(*args, **kwargs)


class Notification(models.Model):
    """
    Modèle pour les notifications utilisateur
    """
    TYPE_CHOICES = [
        ('confirmation', 'Confirmation'),
        ('rappel', 'Rappel'),
        ('modification', 'Modification'),
        ('annulation', 'Annulation'),
    ]
    
    utilisateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name="Utilisateur"
    )
    
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name='notifications',
        null=True,
        blank=True,
        verbose_name="Réservation"
    )
    
    type_notification = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name="Type"
    )
    
    message = models.TextField(
        verbose_name="Message"
    )
    
    est_lue = models.BooleanField(
        default=False,
        verbose_name="Est lue"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date d'envoi"
    )
    
    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['utilisateur', 'est_lue']),
        ]
    
    def __str__(self):
        return f"{self.get_type_notification_display()} - {self.utilisateur.get_full_name()}"
    
    def marquer_comme_lue(self):
        """Marque la notification comme lue"""
        self.est_lue = True
        self.save()


class Rapport(models.Model):
    """
    Modèle pour les rapports statistiques
    """
    TYPE_CHOICES = [
        ('utilisation', 'Utilisation'),
        ('statistiques', 'Statistiques'),
        ('occupation', 'Occupation'),
    ]
    
    administrateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='rapports_crees',
        limit_choices_to={'is_staff': True},
        verbose_name="Administrateur"
    )
    
    titre = models.CharField(
        max_length=200,
        verbose_name="Titre"
    )
    
    type_rapport = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name="Type"
    )
    
    date_debut = models.DateField(
        verbose_name="Date de début"
    )
    
    date_fin = models.DateField(
        verbose_name="Date de fin"
    )
    
    donnees = models.JSONField(
        default=dict,
        verbose_name="Données",
        help_text="Données statistiques du rapport"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de génération"
    )
    
    class Meta:
        verbose_name = "Rapport"
        verbose_name_plural = "Rapports"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.titre} ({self.created_at.date()})"