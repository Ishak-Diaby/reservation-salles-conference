# 🏛️ Système de Réservation de Salles - Django avec Templates

## ✅ PROJET COMPLET AVEC DJANGO TEMPLATES

Version finale du projet utilisant **Django** avec son système de **templates natif** (pas Streamlit) !

---

## 🎯 Architecture Complète Django

### Backend + Frontend Intégré
```
Django MVT (Model-View-Template)
├── Models      → Base de données (5 modèles)
├── Views       → Logique métier (15+ views)
└── Templates   → Interface utilisateur (15+ templates Bootstrap 5)
```

### Pas d'API REST séparée !
- **Interface web native Django**
- **Templates Bootstrap 5** modernes
- **Forms Django** avec validation
- **Messages Framework** pour notifications flash
- **Context processors** pour données globales

---

## 📁 Structure du Projet

```
reservation-salles-conference/
├── config/                     # Configuration Django
│   ├── settings.py            # Settings avec templates
│   ├── urls.py                # URLs principales
│   ├── wsgi.py
│   └── asgi.py
├── reservations/              # Application principale
│   ├── models.py              # 5 modèles Django
│   ├── views.py               # 15+ views
│   ├── forms.py               # 7 forms Django
│   ├── urls.py                # Routes de l'app
│   ├── admin.py               # Admin Django
│   ├── signals.py             # Signaux
│   ├── context_processors.py # Contexte global
│   └── templates/             # Templates Django
│       └── reservations/
│           ├── login.html
│           ├── dashboard.html
│           ├── salles/
│           ├── reservations/
│           ├── notifications/
│           └── admin/
├── templates/
│   └── base.html              # Template de base
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── manage.py
└── db.sqlite3
```

---

## 🚀 Installation et Démarrage

### 1. Installer les dépendances
```bash
pip install Django==5.0.0
pip install django-bootstrap5
pip install django-crispy-forms
pip install crispy-bootstrap5
pip install django-widget-tweaks
```

### 2. Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Créer un superuser
```bash
python manage.py createsuperuser
```

### 4. Charger des données de test (optionnel)
```bash
python manage.py loaddata initial_data.json
```

### 5. Lancer le serveur
```bash
python manage.py runserver
```

### 6. Accéder à l'application
- **Interface web:** http://localhost:8000
- **Admin Django:** http://localhost:8000/admin/

---

## 🎨 Interface Web (Django Templates)

### Pages Publiques
✅ **Page de connexion** (`/`)
✅ **Page d'inscription** (`/inscription/`)

### Pages Utilisateur (Authentifié)
✅ **Tableau de bord** (`/dashboard/`)
✅ **Liste des salles** (`/salles/`)
✅ **Détail d'une salle** (`/salles/<id>/`)
✅ **Recherche de salles** (`/salles/recherche/`)
✅ **Créer une réservation** (`/reservations/creer/`)
✅ **Mes réservations** (`/reservations/mes-reservations/`)
✅ **Détail réservation** (`/reservations/<id>/`)
✅ **Annuler réservation** (`/reservations/<id>/annuler/`)
✅ **Mes notifications** (`/notifications/`)

### Pages Admin
✅ **Dashboard admin** (`/admin-panel/`)
✅ **Gestion des salles** (`/admin-panel/salles/`)
✅ **Créer une salle** (`/admin-panel/salles/creer/`)
✅ **Validation réservations** (`/admin-panel/validation/`)
✅ **Générer rapport** (`/admin-panel/rapports/generer/`)
✅ **Détail rapport** (`/admin-panel/rapports/<id>/`)

---

## 🔑 Fonctionnalités Clés

### 1. Authentification Django
```python
# Login view
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(...)
            login(request, user)
            return redirect('dashboard')
```

### 2. Forms Django avec Validation
```python
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['salle', 'date_reservation', ...]
        widgets = {
            'date_reservation': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            })
        }
```

### 3. Templates Bootstrap 5
```html
{% extends 'base.html' %}

{% block content %}
<div class="container">
    <h1>{{ title }}</h1>
    <!-- Contenu -->
</div>
{% endblock %}
```

### 4. Messages Flash
```python
# Dans la view
messages.success(request, 'Réservation créée avec succès')

# Dans le template
{% if messages %}
    {% for message in messages %}
        <div class="alert alert-{{ message.tags }}">
            {{ message }}
        </div>
    {% endfor %}
{% endif %}
```

### 5. Context Processor
```python
# context_processors.py
def notifications_count(request):
    if request.user.is_authenticated:
        count = Notification.objects.filter(
            utilisateur=request.user,
            est_lue=False
        ).count()
        return {'notifications_non_lues': count}
```

---

## 🎯 Avantages Django Templates vs Streamlit

### Django Templates
✅ **Natif Django** - Parfaitement intégré
✅ **Bootstrap 5** - Design professionnel
✅ **Forms Django** - Validation automatique
✅ **Messages Framework** - Notifications élégantes
✅ **Template Tags** - Logique dans templates
✅ **Static Files** - CSS/JS personnalisés
✅ **SEO Friendly** - URLs propres
✅ **Production Ready** - Scalable

### Streamlit (Moins adapté)
❌ Conçu pour data science, pas web apps
❌ Interface séparée du backend
❌ Pas de vrai système de routing
❌ Moins de contrôle sur le design
❌ Pas adapté pour production

---

## 📊 Technologies Utilisées

### Core
- **Django 5.0** - Framework web
- **SQLite** - Base de données
- **Bootstrap 5** - Framework CSS
- **Bootstrap Icons** - Icônes

### Django Packages
- **django-bootstrap5** - Intégration Bootstrap
- **django-crispy-forms** - Forms stylés
- **crispy-bootstrap5** - Bootstrap 5 pour crispy
- **django-widget-tweaks** - Widgets personnalisés

---

## 🔐 Fonctionnalités Implémentées

### Utilisateurs
✅ Inscription/Connexion/Déconnexion
✅ 3 types: Étudiant, Professeur, Administrateur
✅ Profil utilisateur

### Salles
✅ Liste et détail des salles
✅ Recherche avancée (date, heure, capacité, type)
✅ Affichage des équipements
✅ Gestion admin (CRUD)

### Réservations
✅ Création de réservation
✅ Validation automatique (professeurs)
✅ Validation manuelle (étudiants → admin)
✅ Modification (>2h avant)
✅ Annulation (>2h avant)
✅ Filtres par statut

### Notifications
✅ Création automatique (signaux Django)
✅ Types: confirmation, rappel, modification, annulation
✅ Badge de compteur
✅ Marquer comme lue

### Rapports (Admin)
✅ Génération de statistiques
✅ Période personnalisée
✅ Données: total, par statut, par type utilisateur
✅ Salles les plus populaires

---

## 🎨 Design et UX

### Interface
- **Navbar Bootstrap** responsive
- **Cards** pour les contenus
- **Badges** pour les compteurs
- **Alerts** pour les messages
- **Forms** avec validation
- **Tables** pour les listes
- **Icons** Bootstrap Icons

### Couleurs
- **Primary** (Bleu) - Actions principales
- **Success** (Vert) - Confirmations
- **Warning** (Jaune) - En attente
- **Danger** (Rouge) - Erreurs/Annulations
- **Info** (Cyan) - Informations

---

## 📝 Exemples de Code

### View Django
```python
@login_required
def creer_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST, user=request.user)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.utilisateur = request.user
            reservation.save()
            messages.success(request, 'Réservation créée !')
            return redirect('mes_reservations')
    else:
        form = ReservationForm(user=request.user)
    
    return render(request, 'reservations/creer.html', {'form': form})
```

### Template
```html
{% extends 'base.html' %}

{% block content %}
<div class="container">
    <h1>Nouvelle réservation</h1>
    
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit" class="btn btn-primary">
            Réserver
        </button>
    </form>
</div>
{% endblock %}
```

### Form Django
```python
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['salle', 'date_reservation', 'heure_debut', 
                  'heure_fin', 'motif', 'nombre_participants']
    
    def clean(self):
        # Validation personnalisée
        cleaned_data = super().clean()
        # ...
        return cleaned_data
```

---

## 🎉 Résultat Final

### Ce qui a été livré
✅ **Application Django complète** avec templates
✅ **15+ pages web** fonctionnelles
✅ **Interface Bootstrap 5** moderne
✅ **7 forms Django** avec validation
✅ **15+ views** avec logique métier
✅ **Système de notifications** intégré
✅ **Admin Django** personnalisé
✅ **Documentation UML** complète

### Prêt pour Production
✅ Architecture Django MVT
✅ Sécurité intégrée (CSRF, XSS, SQL injection)
✅ Design responsive
✅ Code professionnel
✅ Extensible et maintenable

---

## 🚀 Déploiement

### Développement
```bash
python manage.py runserver
```

### Production
1. Configure `ALLOWED_HOSTS`
2. Change `SECRET_KEY`
3. Set `DEBUG = False`
4. Configure static files
5. Use PostgreSQL/MySQL
6. Deploy avec Gunicorn + Nginx

---

**Framework:** Django 5.0 avec Templates
**Design:** Bootstrap 5
**Statut:** ✅ Complet et Fonctionnel
**Type:** Application Web Native Django

**C'est la vraie approche Django ! 🎊**