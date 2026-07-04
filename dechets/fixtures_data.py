"""
Script pour peupler la base avec des données de démonstration.
Lancer avec : python fixtures_data.py
"""
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from zones.models import Commune, Quartier
from signalements.models import Signalement
from collectes.models import Vehicule, TourneeCollecte

# Superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@dechets.sn', 'Admin123!')
    print('Superuser admin créé (mot de passe: Admin123!)')

admin = User.objects.get(username='admin')

# Communes
dakar, _ = Commune.objects.get_or_create(nom='Dakar', code='DK', defaults={'population': 1200000})
pikine, _ = Commune.objects.get_or_create(nom='Pikine', code='PK', defaults={'population': 900000})
guediawaye, _ = Commune.objects.get_or_create(nom='Guédiawaye', code='GW', defaults={'population': 350000})

# Quartiers
medina, _ = Quartier.objects.get_or_create(nom='Médina', commune=dakar, defaults={'latitude': 14.6928, 'longitude': -17.4467})
plateau, _ = Quartier.objects.get_or_create(nom='Plateau', commune=dakar, defaults={'latitude': 14.6937, 'longitude': -17.4441})
thiaroye, _ = Quartier.objects.get_or_create(nom='Thiaroye', commune=pikine, defaults={'latitude': 14.7461, 'longitude': -17.3842})
sam, _ = Quartier.objects.get_or_create(nom='Sam Notaire', commune=guediawaye, defaults={'latitude': 14.7789, 'longitude': -17.3998})

# Véhicules
v1, _ = Vehicule.objects.get_or_create(immatriculation='DK-2024-AA', defaults={'type_vehicule': 'camion', 'capacite_tonnes': 5})
v2, _ = Vehicule.objects.get_or_create(immatriculation='DK-2024-BB', defaults={'type_vehicule': 'moto', 'capacite_tonnes': 0.5})
v3, _ = Vehicule.objects.get_or_create(immatriculation='PK-2024-CC', defaults={'type_vehicule': 'tracteur', 'capacite_tonnes': 10})

# Signalements
signalements = [
    {'quartier': medina, 'type_dechet': 'menager', 'niveau_urgence': 'urgent', 'description': 'Grand dépôt de déchets ménagers devant le marché', 'latitude': 14.6928, 'longitude': -17.4467, 'adresse_description': 'Devant marché Sandaga'},
    {'quartier': thiaroye, 'type_dechet': 'encombrant', 'niveau_urgence': 'moyen', 'description': 'Vieux matelas et meubles abandonnés', 'adresse_description': 'Rue 12, côté mosquée'},
    {'quartier': plateau, 'type_dechet': 'construction', 'niveau_urgence': 'faible', 'description': 'Gravats de construction sur le trottoir', 'adresse_description': 'Avenue Faidherbe'},
    {'quartier': sam, 'type_dechet': 'liquide', 'niveau_urgence': 'critique', 'description': 'Déversement de produits chimiques, odeur forte', 'latitude': 14.7789, 'longitude': -17.3998, 'adresse_description': 'Zone industrielle Sam'},
]

for data in signalements:
    Signalement.objects.get_or_create(
        quartier=data['quartier'],
        type_dechet=data['type_dechet'],
        defaults={**data, 'signale_par': admin}
    )

# Tournée de collecte
t, _ = TourneeCollecte.objects.get_or_create(
    titre='Tournée Médina - Semaine 27',
    defaults={
        'date_prevue': '2026-07-01',
        'vehicule': v1,
        'agent_responsable': admin,
        'notes': 'Priorité aux signalements urgents',
    }
)
# Ajouter les signalements à la tournée
for s in Signalement.objects.filter(quartier__commune=dakar):
    t.signalements.add(s)

print('✅ Données de démonstration créées avec succès!')
print(f'   Communes: {Commune.objects.count()}')
print(f'   Quartiers: {Quartier.objects.count()}')
print(f'   Signalements: {Signalement.objects.count()}')
print(f'   Véhicules: {Vehicule.objects.count()}')
print(f'   Tournées: {TourneeCollecte.objects.count()}')
print()
print('➡️  Lancez le serveur: python manage.py runserver')
print('➡️  Swagger: http://127.0.0.1:8000/swagger/')
print('➡️  Login: admin / Admin123!')
