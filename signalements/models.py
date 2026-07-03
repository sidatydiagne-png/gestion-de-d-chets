from django.conf import settings
from django.db import models


class Signalement(models.Model):
    """
    Le cœur du système : un citoyen signale un dépôt sauvage de déchets.
    
    Cycle de vie du statut :
    nouveau → en_cours → résolu
                       ↘ rejeté
    """
    class TypeDechet(models.TextChoices):
        MENAGER = 'menager', 'Déchets ménagers'
        ENCOMBRANT = 'encombrant', 'Encombrants (meubles, électros)'
        CONSTRUCTION = 'construction', 'Gravats / Construction'
        INDUSTRIEL = 'industriel', 'Déchets industriels'
        LIQUIDE = 'liquide', 'Déchets liquides / chimiques'
        AUTRE = 'autre', 'Autre'

    class NiveauUrgence(models.TextChoices):
        FAIBLE = 'faible', 'Faible'
        MOYEN = 'moyen', 'Moyen'
        URGENT = 'urgent', 'Urgent'
        CRITIQUE = 'critique', 'Critique (danger sanitaire)'

    class Statut(models.TextChoices):
        NOUVEAU = 'nouveau', 'Nouveau'
        EN_COURS = 'en_cours', 'En cours de traitement'
        RESOLU = 'resolu', 'Résolu'
        REJETE = 'rejete', 'Rejeté (faux signalement)'

    # Qui signale
    signale_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='signalements',
    )

    # Où (localisation précise)
    quartier = models.ForeignKey(
        'zones.Quartier',
        on_delete=models.PROTECT,
        related_name='signalements',
    )
    # Coordonnées GPS exactes du dépôt (optionnel, si l'utilisateur active la géoloc)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    adresse_description = models.CharField(
        max_length=255, blank=True,
        help_text="Description textuelle de l'emplacement (ex: 'Devant le marché, côté est')"
    )

    # Quoi
    type_dechet = models.CharField(max_length=20, choices=TypeDechet.choices, default=TypeDechet.MENAGER)
    niveau_urgence = models.CharField(max_length=10, choices=NiveauUrgence.choices, default=NiveauUrgence.MOYEN)
    description = models.TextField(help_text="Description détaillée du dépôt")

    # Preuve photo (fonctionnalité principale demandée)
    photo = models.ImageField(
        upload_to='signalements/%Y/%m/',
        null=True, blank=True,
        help_text="Photo du dépôt sauvage"
    )

    # Suivi
    statut = models.CharField(max_length=20, choices=Statut.choices, default=Statut.NOUVEAU)
    traite_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='signalements_traites',
    )
    commentaire_traitement = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolu_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Signalement #{self.id} - {self.quartier} - {self.get_type_dechet_display()}"


class PhotoSupplementaire(models.Model):
    """
    Un signalement peut avoir plusieurs photos (la principale + des supplémentaires).
    """
    signalement = models.ForeignKey(
        Signalement, on_delete=models.CASCADE, related_name='photos_supp'
    )
    photo = models.ImageField(upload_to='signalements/supp/%Y/%m/')
    legende = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo #{self.id} - Signalement #{self.signalement_id}"
