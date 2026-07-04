from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Vehicule, TourneeCollecte
from .serializers import VehiculeSerializer, TourneeCollecteSerializer


class VehiculeViewSet(viewsets.ModelViewSet):
    queryset = Vehicule.objects.all()
    serializer_class = VehiculeSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['disponible', 'type_vehicule']


class TourneeCollecteViewSet(viewsets.ModelViewSet):
    queryset = TourneeCollecte.objects.prefetch_related('signalements').select_related('vehicule', 'agent_responsable').all()
    serializer_class = TourneeCollecteSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['statut', 'date_prevue', 'vehicule', 'agent_responsable']
    ordering_fields = ['date_prevue', 'statut']

    @action(detail=True, methods=['post'])
    def demarrer(self, request, pk=None):
        """Démarre une tournée planifiée → statut passe à en_cours."""
        tournee = self.get_object()
        if tournee.statut != 'planifiee':
            return Response(
                {'detail': 'Seule une tournée planifiée peut être démarrée.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        tournee.statut = 'en_cours'
        tournee.save()
        # Marquer les signalements associés comme en_cours
        tournee.signalements.filter(statut='nouveau').update(statut='en_cours')
        return Response(TourneeCollecteSerializer(tournee).data)

    @action(detail=True, methods=['post'])
    def terminer(self, request, pk=None):
        """Termine une tournée → résout tous les signalements associés."""
        tournee = self.get_object()
        if tournee.statut != 'en_cours':
            return Response(
                {'detail': 'Seule une tournée en cours peut être terminée.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        now = timezone.now()
        tournee.statut = 'terminee'
        tournee.terminee_at = now
        tournee.save()
        # Résoudre automatiquement tous les signalements de la tournée
        tournee.signalements.filter(statut='en_cours').update(
            statut='resolu', resolu_at=now
        )
        # Remettre le véhicule disponible
        if tournee.vehicule:
            tournee.vehicule.disponible = True
            tournee.vehicule.save()
        return Response(TourneeCollecteSerializer(tournee).data)

    @action(detail=False, methods=['get'])
    def planning(self, request):
        """Vue planning : tournées à venir, triées par date."""
        qs = TourneeCollecte.objects.filter(
            statut__in=['planifiee', 'en_cours']
        ).order_by('date_prevue')
        return Response(TourneeCollecteSerializer(qs, many=True).data)
