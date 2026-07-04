from django.contrib import admin
from .models import Commune, Quartier

@admin.register(Commune)
class CommuneAdmin(admin.ModelAdmin):
    list_display = ['nom', 'code', 'population']
    search_fields = ['nom', 'code']

@admin.register(Quartier)
class QuartierAdmin(admin.ModelAdmin):
    list_display = ['nom', 'commune', 'niveau_risque']
    list_filter = ['commune', 'niveau_risque']
    search_fields = ['nom']
