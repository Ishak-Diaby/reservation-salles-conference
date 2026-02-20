"""
Context processors pour ajouter des variables à tous les templates
"""
from .models import Notification


def notifications_count(request):
    """Ajoute le nombre de notifications non lues dans le contexte"""
    if request.user.is_authenticated:
        count = Notification.objects.filter(
            utilisateur=request.user,
            est_lue=False
        ).count()
        return {'notifications_non_lues': count}
    return {'notifications_non_lues': 0}