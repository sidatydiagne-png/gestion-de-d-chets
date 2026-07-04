from rest_framework import serializers
from .models import Commune, Quartier


class CommuneSerializer(serializers.ModelSerializer):
    nb_quartiers = serializers.SerializerMethodField()
    nb_signalements_actifs = serializers.SerializerMethodField()

    class Meta:
        model = Commune
        fields = ['id', 'nom', 'code', 'population', 'superficie_km2',
                  'nb_quartiers', 'nb_signalements_actifs', 'created_at']
        read_only_fields = ['created_at']

    def get_nb_quartiers(self, obj):
        return obj.quartiers.count()

    def get_nb_signalements_actifs(self, obj):
        from signalements.models import Signalement
        return Signalement.objects.filter(
            quartier__commune=obj,
            statut__in=['nouveau', 'en_cours']
        ).count()


class QuartierSerializer(serializers.ModelSerializer):
    commune_nom = serializers.ReadOnlyField(source='commune.nom')
    nb_signalements = serializers.SerializerMethodField()
    niveau_risque_display = serializers.ReadOnlyField(source='get_niveau_risque_display')

    class Meta:
        model = Quartier
        fields = ['id', 'commune', 'commune_nom', 'nom', 'latitude', 'longitude',
                  'niveau_risque', 'niveau_risque_display', 'nb_signalements', 'created_at']
        read_only_fields = ['niveau_risque', 'created_at']

    def get_nb_signalements(self, obj):
        return obj.signalements.filter(statut__in=['nouveau', 'en_cours']).count()
