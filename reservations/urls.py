"""
URLs pour l'application reservations
"""
from django.urls import path
from . import views

urlpatterns = [
    # Authentification
    path('', views.login_view, name='login'),
    path('inscription/', views.inscription_view, name='inscription'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Salles
    path('salles/', views.liste_salles, name='liste_salles'),
    path('salles/<int:pk>/', views.detail_salle, name='detail_salle'),
    path('salles/recherche/', views.rechercher_salles, name='rechercher_salles'),
    
    # Réservations
    path('reservations/creer/', views.creer_reservation, name='creer_reservation'),
    path('reservations/creer/<int:salle_id>/', views.creer_reservation, name='creer_reservation_salle'),
    path('reservations/mes-reservations/', views.mes_reservations, name='mes_reservations'),
    path('reservations/<int:pk>/', views.detail_reservation, name='detail_reservation'),
    path('reservations/<int:pk>/annuler/', views.annuler_reservation, name='annuler_reservation'),
    
    # Notifications
    path('notifications/', views.liste_notifications, name='liste_notifications'),
    path('notifications/<int:pk>/lire/', views.marquer_notification_lue, name='marquer_notification_lue'),
    path('notifications/toutes-lues/', views.marquer_toutes_lues, name='marquer_toutes_lues'),
    
    # Administration
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/salles/', views.gestion_salles, name='gestion_salles'),
    path('admin-panel/salles/creer/', views.creer_salle, name='creer_salle'),
    path('admin-panel/validation/', views.validation_reservations, name='validation_reservations'),
    path('admin-panel/reservations/<int:pk>/valider/', views.valider_reservation, name='valider_reservation'),
    path('admin-panel/reservations/<int:pk>/refuser/', views.refuser_reservation, name='refuser_reservation'),
    path('admin-panel/rapports/generer/', views.generer_rapport, name='generer_rapport'),
    path('admin-panel/rapports/<int:pk>/', views.detail_rapport, name='detail_rapport'),
]