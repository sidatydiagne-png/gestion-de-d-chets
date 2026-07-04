from django.contrib import admin
from .models import Signalement, PhotoSupplementaire

class PhotoInline(admin.TabularInline):
    model = PhotoSupplementaire
    extra = 1

@admin.register(Signalement)
class SignalementAdmin(admin.ModelAdmin):
    list_display = ['id', 'quartier', 'type_dechet', 'niveau_urgence', 'statut', 'created_at']
    list_filter = ['statut', 'type_dechet', 'niveau_urgence']
    search_fields = ['description', 'adresse_description']
    inlines = [PhotoInline]
