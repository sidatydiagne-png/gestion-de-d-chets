from rest_framework import serializers
from .models import Vehicule, TourneeCollecte
from signalements.serializers import SignalementSerializer


class VehiculeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicule
        fields = ['id', 'immatriculation', 'type_vehicule', 'capacite_tonnes', 'disponible']


class TourneeCollecteSerializer(serializers.ModelSerializer):
    nb_signalements = serializers.ReadOnlyField()
    statut_display = serializers.ReadOnlyField(source='get_statut_display')
    vehicule_detail = VehiculeSerializer(source='vehicule', read_only=True)
    agent_username = serializers.ReadOnlyField(source='agent_responsable.username')

    class Meta:
        model = TourneeCollecte
        fields = [
            'id', 'titre', 'date_prevue', 'statut', 'statut_display',
            'vehicule', 'vehicule_detail', 'agent_responsable', 'agent_username',
            'signalements', 'nb_signalements',
            'notes', 'created_at', 'terminee_at',
        ]
        read_only_fields = ['created_at', 'terminee_at']
