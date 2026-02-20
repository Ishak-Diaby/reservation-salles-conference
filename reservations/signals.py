"""
Signaux Django pour automatiser certaines actions
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Reservation, Notification


@receiver(post_save, sender=Reservation)
def creer_notification_reservation(sender, instance, created, **kwargs):
    """
    Crée automatiquement une notification lors de la création/modification d'une réservation
    """
    if created:
        # Nouvelle réservation
        message = f"Réservation {instance.get_statut_display()} pour la salle {instance.salle.nom} le {instance.date_reservation} de {instance.heure_debut} à {instance.heure_fin}"
        
        Notification.objects.create(
            utilisateur=instance.utilisateur,
            reservation=instance,
            type_notification='confirmation',
            message=message
        )
    else:
        # Réservation modifiée
        # Note: Pour détecter les changements de statut précis, on pourrait utiliser django-model-utils
        # Pour l'instant, on crée une notification générique pour toute modification
        message = f"Votre réservation de la salle {instance.salle.nom} le {instance.date_reservation} a été mise à jour - Statut: {instance.get_statut_display()}"
        type_notif = 'modification'
        
        Notification.objects.create(
            utilisateur=instance.utilisateur,
            reservation=instance,
            type_notification=type_notif,
            message=message
        )