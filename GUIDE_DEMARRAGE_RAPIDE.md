# 🚀 Guide de Démarrage Rapide

## ✅ Tous les Fichiers Sont Présents !

### Fichiers Essentiels Créés

✅ **manage.py** - Command-line Django
✅ **config/settings.py** - Configuration complète
✅ **config/urls.py** - URLs principales  
✅ **config/wsgi.py** - WSGI application
✅ **config/asgi.py** - ASGI application
✅ **config/__init__.py**

✅ **reservations/models.py** - 5 modèles Django
✅ **reservations/views.py** - 15+ views
✅ **reservations/forms.py** - 7 forms
✅ **reservations/urls.py** - Routes
✅ **reservations/admin.py** - Admin Django
✅ **reservations/signals.py** - Signaux
✅ **reservations/apps.py** - Configuration
✅ **reservations/__init__.py**
✅ **reservations/context_processors.py**

✅ **templates/base.html** - Template de base
✅ **reservations/templates/reservations/login.html**
✅ **reservations/templates/reservations/dashboard.html**

✅ **static/css/style.css** - Styles personnalisés
✅ **static/js/main.js** - Scripts JavaScript

✅ **requirements.txt** - Dépendances
✅ **.gitignore**

---

## 🎯 Installation en 5 Étapes

### 1️⃣ Installer les Dépendances

```bash
pip install -r requirements.txt
```

**Packages installés:**
- Django 5.0.0
- django-bootstrap5
- django-crispy-forms
- crispy-bootstrap5
- django-widget-tweaks

### 2️⃣ Créer les Migrations

```bash
python manage.py makemigrations
```

**Résultat attendu:**
```
Migrations for 'reservations':
  reservations/migrations/0001_initial.py
    - Create model Utilisateur
    - Create model Salle
    - Create model Reservation
    - Create model Notification
    - Create model Rapport
```

### 3️⃣ Appliquer les Migrations

```bash
python manage.py migrate
```

**Résultat attendu:**
```
Applying reservations.0001_initial... OK
```

### 4️⃣ Créer un Superuser

```bash
python manage.py createsuperuser
```

**Saisir:**
- Username: admin
- Email: admin@universite.fr
- Password: admin (ou votre choix)

### 5️⃣ Lancer le Serveur

```bash
python manage.py runserver
```

**Serveur démarre sur:** http://localhost:8000

---

## 🌐 Accéder à l'Application

### Interface Web
**URL:** http://localhost:8000
**Page:** Connexion

### Admin Django
**URL:** http://localhost:8000/admin/
**Login:** admin / admin

---

## 📝 Premiers Tests

### Test 1: Admin Django

1. Allez sur http://localhost:8000/admin/
2. Connectez-vous avec le superuser
3. Vous verrez:
   - Utilisateurs
   - Salles
   - Réservations
   - Notifications
   - Rapports

### Test 2: Créer des Données

**Dans l'admin, créez:**

1. **Un utilisateur étudiant:**
   - Type: Étudiant
   - Niveau: L3
   
2. **Un utilisateur professeur:**
   - Type: Professeur
   - Département: Informatique

3. **Quelques salles:**
   - Amphi A (Amphithéâtre, 200 places)
   - TD 101 (Salle TD, 40 places)
   - TP Info 1 (Salle TP, 25 places)

### Test 3: Interface Web

1. Allez sur http://localhost:8000
2. Connectez-vous avec un utilisateur
3. Explorez le dashboard

---

## 🔧 Commandes Utiles

### Créer un utilisateur en shell
```bash
python manage.py shell
```

```python
from reservations.models import Utilisateur
user = Utilisateur.objects.create_user(
    username='etudiant',
    email='etudiant@universite.fr',
    password='etudiant123',
    first_name='Pierre',
    last_name='Dupont',
    type_utilisateur='etudiant',
    niveau='L3'
)
```

### Créer des salles en shell
```python
from reservations.models import Salle

Salle.objects.create(
    nom='Amphi A',
    batiment='Bâtiment Principal',
    etage=0,
    capacite=200,
    type_salle='amphi',
    equipements=['Vidéoprojecteur', 'Microphone', 'Écran'],
    description='Grand amphithéâtre pour cours magistraux'
)
```

### Vérifier les models
```bash
python manage.py check
```

### Afficher les migrations
```bash
python manage.py showmigrations
```

### Collectstatic (pour production)
```bash
python manage.py collectstatic
```

---

## ⚠️ Problèmes Courants

### ImportError: No module named 'reservations'

**Solution:**
```bash
# Vérifier que vous êtes dans le bon dossier
pwd
# Doit afficher: .../django-reservation

# Vérifier INSTALLED_APPS dans settings.py
# 'reservations' doit être dans la liste
```

### Table doesn't exist

**Solution:**
```bash
python manage.py makemigrations
python manage.py migrate
```

### Static files not loading

**Solution:**
```bash
# En développement, vérifier settings.py:
DEBUG = True

# Puis relancer le serveur
python manage.py runserver
```

---

## 🎨 Personnalisation

### Changer les couleurs
Éditer: `static/css/style.css`

```css
:root {
    --primary-color: #votre-couleur;
}
```

### Ajouter un logo
1. Mettre l'image dans `static/images/`
2. Dans `base.html`:
```html
<img src="{% static 'images/logo.png' %}" alt="Logo">
```

---

## 📱 Prochaines Étapes

### Templates à Créer (Optionnel)

Pour avoir toutes les pages:
1. inscription.html
2. salles/liste.html
3. salles/detail.html
4. salles/recherche.html
5. reservations/creer.html
6. reservations/mes_reservations.html
7. notifications/liste.html
8. admin/*.html

**Note:** L'application fonctionne déjà avec les templates de base créés !

### Tests

```bash
python manage.py test
```

### Déploiement

Pour production:
1. DEBUG = False dans settings.py
2. Configurer ALLOWED_HOSTS
3. Utiliser PostgreSQL
4. Configurer Gunicorn + Nginx

---

## ✅ Checklist de Vérification

- [ ] requirements.txt installé
- [ ] Migrations créées
- [ ] Migrations appliquées
- [ ] Superuser créé
- [ ] Serveur démarre sans erreur
- [ ] Admin accessible
- [ ] Login page s'affiche
- [ ] CSS et JS chargés

---

**Tout est prêt ! Bon développement ! 🎉**