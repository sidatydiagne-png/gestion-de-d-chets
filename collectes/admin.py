from django.contrib import admin
from .models import Vehicule, TourneeCollecte

@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
    list_display = ['immatriculation', 'type_vehicule', 'capacite_tonnes', 'disponible']
    list_filter = ['disponible', 'type_vehicule']

@admin.register(TourneeCollecte)
class TourneeAdmin(admin.ModelAdmin):
    list_display = ['titre', 'date_prevue', 'statut', 'vehicule', 'agent_responsable', 'nb_signalements']
    list_filter = ['statut', 'date_prevue']
    filter_horizontal = ['signalements']
