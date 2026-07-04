from django.db import models


class Commune(models.Model):
    """
    Une commune (ex: Dakar, Pikine, Guédiawaye).
    C'est le découpage administratif principal.
    """
    nom = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    population = models.PositiveIntegerField(default=0)
    superficie_km2 = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nom']

    def __str__(self):
        return self.nom


class Quartier(models.Model):
    """
    Un quartier appartient à une commune.
    C'est l'unité géographique fine pour localiser les incidents.
    """
    class NiveauRisque(models.TextChoices):
        FAIBLE = 'faible', 'Faible'
        MOYEN = 'moyen', 'Moyen'
        ELEVE = 'eleve', 'Élevé'
        CRITIQUE = 'critique', 'Critique'

    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, related_name='quartiers')
    nom = models.CharField(max_length=100)
    # Coordonnées GPS du centre du quartier (pour la cartographie)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    niveau_risque = models.CharField(
        max_length=20,
        choices=NiveauRisque.choices,
        default=NiveauRisque.FAIBLE,
        help_text="Calculé automatiquement selon le nombre d'incidents récents"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['commune', 'nom']
        unique_together = ['commune', 'nom']

    def __str__(self):
        return f"{self.nom} ({self.commune.nom})"

    def update_niveau_risque(self):
        """
        Met à jour automatiquement le niveau de risque
        selon le nombre de signalements actifs dans ce quartier.
        """
        from signalements.models import Signalement
        nb = Signalement.objects.filter(
            quartier=self,
            statut__in=['nouveau', 'en_cours']
        ).count()
        if nb == 0:
            self.niveau_risque = self.NiveauRisque.FAIBLE
        elif nb <= 3:
            self.niveau_risque = self.NiveauRisque.MOYEN
        elif nb <= 7:
            self.niveau_risque = self.NiveauRisque.ELEVE
        else:
            self.niveau_risque = self.NiveauRisque.CRITIQUE
        self.save()
