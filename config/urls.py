"""
URL Configuration pour le projet de réservation de salles
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('reservations.urls')),
]

# Serve static et media files en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Personnalisation de l'admin Django
admin.site.site_header = "Administration - Réservation de Salles"
admin.site.site_title = "Admin Réservations"
admin.site.index_title = "Gestion du système de réservation"