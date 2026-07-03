from django.conf import settings
from django.db import models


class Vehicule(models.Model):
    """Camion ou véhicule de collecte disponible."""
    class Type(models.TextChoices):
        CAMION = 'camion', 'Camion benne'
        TRACTEUR = 'tracteur', 'Tracteur-remorque'
        MOTO = 'moto', 'Moto-tricycle (petites rues)'

    immatriculation = models.CharField(max_length=20, unique=True)
    type_vehicule = models.CharField(max_length=20, choices=Type.choices)
    capacite_tonnes = models.DecimalField(max_digits=5, decimal_places=2)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.immatriculation} ({self.get_type_vehicule_display()})"


class TourneeCollecte(models.Model):
    """
    Une tournée = un ensemble de signalements à traiter,
    assigné à un véhicule et un agent, planifié à une date.
    """
    class Statut(models.TextChoices):
        PLANIFIEE = 'planifiee', 'Planifiée'
        EN_COURS = 'en_cours', 'En cours'
        TERMINEE = 'terminee', 'Terminée'
        ANNULEE = 'annulee', 'Annulée'

    titre = models.CharField(max_length=200)
    date_prevue = models.DateField()
    statut = models.CharField(max_length=20, choices=Statut.choices, default=Statut.PLANIFIEE)
    vehicule = models.ForeignKey(
        Vehicule, on_delete=models.PROTECT,
        related_name='tournees', null=True, blank=True
    )
    agent_responsable = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='tournees_responsable',
    )
    # Les signalements à collecter dans cette tournée
    signalements = models.ManyToManyField(
        'signalements.Signalement',
        related_name='tournees',
        blank=True,
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    terminee_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['date_prevue']

    def __str__(self):
        return f"{self.titre} - {self.date_prevue}"

    @property
    def nb_signalements(self):
        return self.signalements.count()
