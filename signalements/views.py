from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from .models import Signalement, PhotoSupplementaire
from .serializers import (
    SignalementSerializer,
    SignalementTraitementSerializer,
    StatistiquesSerializer,
)


class SignalementViewSet(viewsets.ModelViewSet):
    """
    ViewSet principal pour les signalements.
    
    list:   GET  /signalements/          → liste tous les signalements
    create: POST /signalements/          → créer un nouveau signalement
    read:   GET  /signalements/{id}/     → détail d'un signalement
    update: PUT  /signalements/{id}/     → modifier
    delete: DELETE /signalements/{id}/   → supprimer
    
    Actions custom:
    traiter:      POST /signalements/{id}/traiter/      → changer le statut
    stats:        GET  /signalements/statistiques/      → tableau de bord
    carte:        GET  /signalements/carte/             → données pour la carte
    urgents:      GET  /signalements/urgents/           → signalements critiques
    """
    queryset = Signalement.objects.select_related('signale_par', 'quartier__commune').all()
    serializer_class = SignalementSerializer
    filterset_fields = ['statut', 'type_dechet', 'niveau_urgence', 'quartier', 'quartier__commune']
    search_fields = ['description', 'adresse_description', 'quartier__nom']
    ordering_fields = ['created_at', 'niveau_urgence', 'statut']

    def get_permissions(self):
        # Les citoyens peuvent consulter et créer des signalements, et voir la carte,
        # sans être connectés. Traiter/modifier/supprimer/statistiques restent réservés
        # aux utilisateurs authentifiés (admin/agents).
        if self.action in ['list', 'retrieve', 'create', 'carte']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    @action(detail=True, methods=['post'])
    def traiter(self, request, pk=None):
        """
        Permet à un agent de changer le statut d'un signalement
        (en_cours, resolu, rejete) avec un commentaire.
        """
        signalement = self.get_object()
        serializer = SignalementTraitementSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        nouveau_statut = serializer.validated_data['statut']
        commentaire = serializer.validated_data.get('commentaire', '')

        signalement.statut = nouveau_statut
        signalement.traite_par = request.user
        signalement.commentaire_traitement = commentaire

        if nouveau_statut == 'resolu':
            signalement.resolu_at = timezone.now()

        signalement.save()
        # Mettre à jour le niveau de risque du quartier
        signalement.quartier.update_niveau_risque()

        return Response(SignalementSerializer(signalement).data)

    @action(detail=False, methods=['get'])
    def statistiques(self, request):
        """
        Tableau de bord : totaux par statut, par type de déchet, par urgence, par commune.
        """
        from django.db.models import Count
        from zones.models import Commune

        qs = Signalement.objects.all()

        # Totaux par statut
        par_statut = {s: qs.filter(statut=s).count() for s in ['nouveau', 'en_cours', 'resolu', 'rejete']}

        # Totaux par type de déchet
        par_type = {
            t: qs.filter(type_dechet=t).count()
            for t, _ in Signalement.TypeDechet.choices
        }

        # Totaux par urgence
        par_urgence = {
            u: qs.filter(niveau_urgence=u).count()
            for u, _ in Signalement.NiveauUrgence.choices
        }

        # Totaux par commune
        par_commune = list(
            qs.values('quartier__commune__nom')
            .annotate(total=Count('id'))
            .order_by('-total')
        )

        data = {
            'total_signalements': qs.count(),
            'nouveaux': par_statut['nouveau'],
            'en_cours': par_statut['en_cours'],
            'resolus': par_statut['resolu'],
            'rejetes': par_statut['rejete'],
            'par_type': par_type,
            'par_urgence': par_urgence,
            'par_commune': par_commune,
        }
        return Response(data)

    @action(detail=False, methods=['get'])
    def carte(self, request):
        """
        Renvoie les données géolocalisées pour afficher les points sur une carte.
        Chaque signalement actif avec coordonnées GPS est inclus.
        """
        qs = Signalement.objects.filter(
            statut__in=['nouveau', 'en_cours'],
        ).exclude(latitude=None).select_related('quartier__commune')

        data = [
            {
                'id': s.id,
                'latitude': float(s.latitude),
                'longitude': float(s.longitude),
                'type_dechet': s.get_type_dechet_display(),
                'niveau_urgence': s.niveau_urgence,
                'quartier': str(s.quartier),
                'statut': s.statut,
                'photo': s.photo.url if s.photo else None,
            }
            for s in qs
        ]
        return Response({'count': len(data), 'points': data})

    @action(detail=False, methods=['get'])
    def urgents(self, request):
        """
        Liste uniquement les signalements urgents ou critiques non résolus.
        Permet aux agents de prioriser leurs interventions.
        """
        qs = self.get_queryset().filter(
            niveau_urgence__in=['urgent', 'critique'],
            statut__in=['nouveau', 'en_cours'],
        ).order_by('-niveau_urgence', 'created_at')

        page = self.paginate_queryset(qs)
        serializer = self.get_serializer(page or qs, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)
