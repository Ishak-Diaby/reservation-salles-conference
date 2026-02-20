"""
Configuration de l'application reservations
"""
from django.apps import AppConfig


class ReservationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reservations'
    verbose_name = "Gestion des Réservations"
    
    def ready(self):
        """Importer les signaux quand l'app est prête"""
        import reservations.signals