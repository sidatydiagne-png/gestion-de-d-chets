from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Commune, Quartier
from .serializers import CommuneSerializer, QuartierSerializer
import django_filters


class CommuneViewSet(viewsets.ModelViewSet):
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['nom', 'code']
    ordering_fields = ['nom', 'population']


class QuartierViewSet(viewsets.ModelViewSet):
    queryset = Quartier.objects.select_related('commune').all()
    serializer_class = QuartierSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['commune', 'niveau_risque']
    search_fields = ['nom', 'commune__nom']
    ordering_fields = ['nom', 'niveau_risque']
