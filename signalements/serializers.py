from rest_framework import serializers
from .models import Signalement, PhotoSupplementaire


class PhotoSupplementaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoSupplementaire
        fields = ['id', 'photo', 'legende', 'uploaded_at']
        read_only_fields = ['uploaded_at']


class SignalementSerializer(serializers.ModelSerializer):
    """
    Serializer principal pour créer et lire un signalement.
    signale_par et statut sont en read_only car gérés automatiquement.
    """
    signale_par_username = serializers.ReadOnlyField(source='signale_par.username')
    quartier_nom = serializers.ReadOnlyField(source='quartier.__str__')
    type_dechet_display = serializers.ReadOnlyField(source='get_type_dechet_display')
    niveau_urgence_display = serializers.ReadOnlyField(source='get_niveau_urgence_display')
    statut_display = serializers.ReadOnlyField(source='get_statut_display')
    photos_supp = PhotoSupplementaireSerializer(many=True, read_only=True)

    class Meta:
        model = Signalement
        fields = [
            'id', 'signale_par', 'signale_par_username',
            'quartier', 'quartier_nom', 'latitude', 'longitude', 'adresse_description',
            'type_dechet', 'type_dechet_display',
            'niveau_urgence', 'niveau_urgence_display',
            'description', 'photo',
            'statut', 'statut_display',
            'traite_par', 'commentaire_traitement',
            'photos_supp', 'created_at', 'updated_at', 'resolu_at',
        ]
        read_only_fields = [
            'signale_par', 'statut', 'traite_par',
            'commentaire_traitement', 'created_at', 'updated_at', 'resolu_at'
        ]

    def create(self, validated_data):
        # On assigne automatiquement l'utilisateur connecté comme auteur du signalement
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['signale_par'] = request.user
        signalement = super().create(validated_data)
        # On met à jour le niveau de risque du quartier automatiquement
        signalement.quartier.update_niveau_risque()
        return signalement


class SignalementTraitementSerializer(serializers.Serializer):
    """
    Utilisé uniquement pour l'action de traitement (résoudre/rejeter).
    On ne demande que le nouveau statut et un commentaire.
    """
    statut = serializers.ChoiceField(choices=['en_cours', 'resolu', 'rejete'])
    commentaire = serializers.CharField(required=False, allow_blank=True)


class StatistiquesSerializer(serializers.Serializer):
    """Serializer pour le tableau de bord statistique."""
    total_signalements = serializers.IntegerField()
    nouveaux = serializers.IntegerField()
    en_cours = serializers.IntegerField()
    resolus = serializers.IntegerField()
    rejetes = serializers.IntegerField()
    par_type = serializers.DictField()
    par_urgence = serializers.DictField()
    par_commune = serializers.ListField()
