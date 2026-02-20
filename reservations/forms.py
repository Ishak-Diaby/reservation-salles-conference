"""
Forms Django pour le système de réservation
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Utilisateur, Salle, Reservation


class LoginForm(forms.Form):
    """Form de connexion"""
    username = forms.CharField(
        label='Nom d\'utilisateur',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre nom d\'utilisateur'
        })
    )
    password = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre mot de passe'
        })
    )


class InscriptionForm(UserCreationForm):
    """Form d'inscription"""
    email = forms.EmailField(required=True)
    
    class Meta:
        model = Utilisateur
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 
                  'password2', 'type_utilisateur', 'niveau', 'departement']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'type_utilisateur': forms.Select(attrs={'class': 'form-select'}),
            'niveau': forms.Select(attrs={'class': 'form-select'}),
            'departement': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


class ReservationForm(forms.ModelForm):
    """Form de création/modification de réservation"""
    
    class Meta:
        model = Reservation
        fields = ['salle', 'date_reservation', 'heure_debut', 'heure_fin', 
                  'motif', 'nombre_participants']
        widgets = {
            'salle': forms.Select(attrs={'class': 'form-select'}),
            'date_reservation': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': '',  # Sera rempli dynamiquement
            }),
            'heure_debut': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'heure_fin': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'motif': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Décrivez le motif de votre réservation...'
            }),
            'nombre_participants': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.salle = kwargs.pop('salle', None)
        super().__init__(*args, **kwargs)
        
        # Limiter les salles disponibles
        self.fields['salle'].queryset = Salle.objects.filter(est_disponible=True)
        
        # Si une salle est pré-sélectionnée
        if self.salle:
            self.fields['salle'].initial = self.salle
            self.fields['salle'].disabled = True
        
        # Date minimale = aujourd'hui
        from datetime import date
        self.fields['date_reservation'].widget.attrs['min'] = date.today().isoformat()


class SalleForm(forms.ModelForm):
    """Form de création/modification de salle (admin)"""
    
    class Meta:
        model = Salle
        fields = ['nom', 'batiment', 'etage', 'capacite', 'type_salle', 
                  'equipements', 'description', 'est_disponible']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'batiment': forms.TextInput(attrs={'class': 'form-control'}),
            'etage': forms.NumberInput(attrs={'class': 'form-control'}),
            'capacite': forms.NumberInput(attrs={'class': 'form-control'}),
            'type_salle': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'est_disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    # Champ pour les équipements (transformé en checkboxes)
    equipement_videoprojecteur = forms.BooleanField(required=False, label='Vidéoprojecteur')
    equipement_ordinateur = forms.BooleanField(required=False, label='Ordinateur')
    equipement_tableau_blanc = forms.BooleanField(required=False, label='Tableau blanc')
    equipement_ecran = forms.BooleanField(required=False, label='Écran')
    equipement_microphone = forms.BooleanField(required=False, label='Microphone')
    equipement_climatisation = forms.BooleanField(required=False, label='Climatisation')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Si on édite une salle existante, pré-cocher les équipements
        if self.instance and self.instance.pk:
            equipements = self.instance.equipements or []
            self.fields['equipement_videoprojecteur'].initial = 'Vidéoprojecteur' in equipements
            self.fields['equipement_ordinateur'].initial = 'Ordinateur' in equipements
            self.fields['equipement_tableau_blanc'].initial = 'Tableau blanc' in equipements
            self.fields['equipement_ecran'].initial = 'Écran' in equipements
            self.fields['equipement_microphone'].initial = 'Microphone' in equipements
            self.fields['equipement_climatisation'].initial = 'Climatisation' in equipements
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Construire la liste des équipements
        equipements = []
        if self.cleaned_data.get('equipement_videoprojecteur'):
            equipements.append('Vidéoprojecteur')
        if self.cleaned_data.get('equipement_ordinateur'):
            equipements.append('Ordinateur')
        if self.cleaned_data.get('equipement_tableau_blanc'):
            equipements.append('Tableau blanc')
        if self.cleaned_data.get('equipement_ecran'):
            equipements.append('Écran')
        if self.cleaned_data.get('equipement_microphone'):
            equipements.append('Microphone')
        if self.cleaned_data.get('equipement_climatisation'):
            equipements.append('Climatisation')
        
        instance.equipements = equipements
        
        if commit:
            instance.save()
        
        return instance


class RechercheForm(forms.Form):
    """Form de recherche de salles disponibles"""
    date_reservation = forms.DateField(
        label='Date',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'min': '',  # Sera rempli par JS
        })
    )
    heure_debut = forms.TimeField(
        label='Heure de début',
        widget=forms.TimeInput(attrs={
            'class': 'form-control',
            'type': 'time'
        })
    )
    heure_fin = forms.TimeField(
        label='Heure de fin',
        widget=forms.TimeInput(attrs={
            'class': 'form-control',
            'type': 'time'
        })
    )
    capacite_min = forms.IntegerField(
        label='Capacité minimale',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: 30'
        })
    )
    type_salle = forms.ChoiceField(
        label='Type de salle',
        required=False,
        choices=[('', 'Tous')] + list(Salle.TYPE_CHOICES),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    batiment = forms.CharField(
        label='Bâtiment',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: Bâtiment A'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from datetime import date
        self.fields['date_reservation'].widget.attrs['min'] = date.today().isoformat()


class RapportForm(forms.Form):
    """Form de génération de rapport (admin)"""
    date_debut = forms.DateField(
        label='Date de début',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    date_fin = forms.DateField(
        label='Date de fin',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        date_debut = cleaned_data.get('date_debut')
        date_fin = cleaned_data.get('date_fin')
        
        if date_debut and date_fin:
            if date_fin < date_debut:
                raise ValidationError('La date de fin doit être après la date de début')
        
        return cleaned_data