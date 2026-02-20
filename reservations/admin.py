"""
Configuration de l'interface d'administration Django
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur, Salle, Reservation, Notification, Rapport


@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    """Administration personnalisée pour Utilisateur"""
    list_display = ['username', 'email', 'first_name', 'last_name', 'type_utilisateur', 'is_active']
    list_filter = ['type_utilisateur', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('type_utilisateur', 'niveau', 'departement')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('type_utilisateur', 'niveau', 'departement')
        }),
    )


@admin.register(Salle)
class SalleAdmin(admin.ModelAdmin):
    """Administration pour Salle"""
    list_display = ['nom', 'batiment', 'etage', 'capacite', 'type_salle', 'est_disponible']
    list_filter = ['type_salle', 'batiment', 'est_disponible']
    search_fields = ['nom', 'batiment']
    list_editable = ['est_disponible']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'batiment', 'etage', 'capacite', 'type_salle')
        }),
        ('Équipements et description', {
            'fields': ('equipements', 'description')
        }),
        ('Disponibilité', {
            'fields': ('est_disponible',)
        }),
    )


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """Administration pour Reservation"""
    list_display = ['salle', 'utilisateur', 'date_reservation', 'heure_debut', 'heure_fin', 'statut', 'created_at']
    list_filter = ['statut', 'date_reservation', 'created_at']
    search_fields = ['salle__nom', 'utilisateur__username', 'motif']
    date_hierarchy = 'date_reservation'
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('utilisateur', 'salle', 'statut')
        }),
        ('Créneau', {
            'fields': ('date_reservation', 'heure_debut', 'heure_fin')
        }),
        ('Détails', {
            'fields': ('motif', 'nombre_participants')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    actions = ['valider_reservations', 'refuser_reservations']
    
    def valider_reservations(self, request, queryset):
        """Action pour valider plusieurs réservations"""
        count = 0
        for reservation in queryset:
            if reservation.statut == 'en_attente':
                reservation.valider()
                count += 1
        self.message_user(request, f"{count} réservation(s) validée(s)")
    valider_reservations.short_description = "Valider les réservations sélectionnées"
    
    def refuser_reservations(self, request, queryset):
        """Action pour refuser plusieurs réservations"""
        count = 0
        for reservation in queryset:
            if reservation.statut == 'en_attente':
                reservation.refuser()
                count += 1
        self.message_user(request, f"{count} réservation(s) refusée(s)")
    refuser_reservations.short_description = "Refuser les réservations sélectionnées"


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Administration pour Notification"""
    list_display = ['utilisateur', 'type_notification', 'message_court', 'created_at', 'est_lue']
    list_filter = ['type_notification', 'est_lue', 'created_at']
    search_fields = ['utilisateur__username', 'message']
    date_hierarchy = 'created_at'
    
    def message_court(self, obj):
        """Affiche un message court"""
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_court.short_description = 'Message'


@admin.register(Rapport)
class RapportAdmin(admin.ModelAdmin):
    """Administration pour Rapport"""
    list_display = ['titre', 'type_rapport', 'date_debut', 'date_fin', 'created_at']
    list_filter = ['type_rapport', 'created_at']
    search_fields = ['titre']
    date_hierarchy = 'created_at'
    
    readonly_fields = ['created_at']