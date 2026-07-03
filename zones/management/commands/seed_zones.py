"""
Commande pour peupler la base avec les grandes communes de la région
de Dakar (celles qui englobent d'autres quartiers/zones) et leurs
principaux quartiers.

Usage : python manage.py seed_zones
"""
from django.core.management.base import BaseCommand
from zones.models import Commune, Quartier


COMMUNES_DAKAR = [
    {
        "nom": "Dakar", "code": "DK", "population": 1200000, "superficie_km2": 82.4,
        "quartiers": [
            ("Plateau", 14.6707, -17.4344),
            ("Médina", 14.6842, -17.4467),
            ("Fann - Point E - Amitié", 14.6928, -17.4633),
            ("Ouakam", 14.7167, -17.4833),
            ("Ngor", 14.7458, -17.5119),
            ("Yoff", 14.7500, -17.4700),
            ("Grand Dakar", 14.7089, -17.4508),
            ("Parcelles Assainies", 14.7550, -17.4225),
            ("HLM", 14.7028, -17.4472),
            ("Grand Yoff", 14.7317, -17.4508),
        ],
    },
    {
        "nom": "Pikine", "code": "PK", "population": 900000, "superficie_km2": 40.0,
        "quartiers": [
            ("Thiaroye", 14.7461, -17.3842),
            ("Guinaw Rails", 14.7622, -17.4014),
            ("Djiddah Thiaroye Kao", 14.7669, -17.3922),
            ("Dalifort", 14.7386, -17.4197),
            ("Pikine Nord", 14.7692, -17.4014),
        ],
    },
    {
        "nom": "Guédiawaye", "code": "GW", "population": 350000, "superficie_km2": 13.3,
        "quartiers": [
            ("Sam Notaire", 14.7789, -17.3998),
            ("Golf", 14.7772, -17.4128),
            ("Wakhinane Nimzatt", 14.7856, -17.3933),
            ("Ndiarème Limamoulaye", 14.7739, -17.4067),
        ],
    },
    {
        "nom": "Rufisque", "code": "RF", "population": 400000, "superficie_km2": 62.9,
        "quartiers": [
            ("Rufisque Nord", 14.7178, -17.2733),
            ("Rufisque Est", 14.7139, -17.2589),
            ("Rufisque Ouest", 14.7222, -17.2825),
            ("Bata Plage", 14.7083, -17.2778),
        ],
    },
    {
        "nom": "Keur Massar", "code": "KM", "population": 500000, "superficie_km2": 60.0,
        "quartiers": [
            ("Keur Massar Nord", 14.7900, -17.3100),
            ("Keur Massar Sud", 14.7750, -17.3200),
            ("Malika", 14.8028, -17.3167),
        ],
    },
    {
        "nom": "Bargny", "code": "BG", "population": 60000, "superficie_km2": 20.0,
        "quartiers": [
            ("Bargny Guedj", 14.6989, -17.2214),
            ("Minam", 14.6944, -17.2306),
            ("Sindiane", 14.7028, -17.2139),
        ],
    },
    {
        "nom": "Diamniadio", "code": "DM", "population": 30000, "superficie_km2": 60.0,
        "quartiers": [
            ("Diamniadio Centre", 14.7167, -17.1833),
            ("Pôle Urbain de Diamniadio", 14.7222, -17.1750),
        ],
    },
    {
        "nom": "Sébikotane", "code": "SB", "population": 25000, "superficie_km2": 45.0,
        "quartiers": [
            ("Sébikotane Centre", 14.7500, -17.1333),
            ("Kessoukhatte", 14.7444, -17.1417),
        ],
    },
    {
        "nom": "Sangalkam", "code": "SG", "population": 45000, "superficie_km2": 70.0,
        "quartiers": [
            ("Sangalkam Centre", 14.7833, -17.2333),
            ("Tivaouane Peulh", 14.8083, -17.2472),
        ],
    },
    {
        "nom": "Bambilor", "code": "BB", "population": 20000, "superficie_km2": 90.0,
        "quartiers": [
            ("Bambilor Centre", 14.8167, -17.2833),
            ("Déni Biram Ndao", 14.8306, -17.2694),
        ],
    },
]


class Command(BaseCommand):
    help = "Peuple la base avec les grandes communes de la région de Dakar et leurs quartiers"

    def handle(self, *args, **options):
        nb_communes_creees = 0
        nb_quartiers_crees = 0

        for c in COMMUNES_DAKAR:
            commune, created = Commune.objects.get_or_create(
                code=c["code"],
                defaults={
                    "nom": c["nom"],
                    "population": c["population"],
                    "superficie_km2": c["superficie_km2"],
                },
            )
            if created:
                nb_communes_creees += 1
                self.stdout.write(self.style.SUCCESS(f"  + Commune créée : {commune.nom}"))
            else:
                self.stdout.write(f"  = Commune déjà existante : {commune.nom}")

            for nom_quartier, lat, lng in c["quartiers"]:
                quartier, q_created = Quartier.objects.get_or_create(
                    commune=commune,
                    nom=nom_quartier,
                    defaults={"latitude": lat, "longitude": lng},
                )
                if q_created:
                    nb_quartiers_crees += 1

        self.stdout.write(self.style.SUCCESS(
            f"\n✅ Terminé : {nb_communes_creees} commune(s) créée(s), "
            f"{nb_quartiers_crees} quartier(s) créé(s)."
        ))
        self.stdout.write(
            f"   Total en base : {Commune.objects.count()} communes, "
            f"{Quartier.objects.count()} quartiers."
        )
