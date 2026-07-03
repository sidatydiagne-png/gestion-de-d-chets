# 🗑️ Système Intelligent de Gestion des Déchets Urbains

Backend Django REST Framework — Examen CAT L2 2025-2026

## 🚀 Installation

```bash
pip install -r requirements.txt
python manage.py migrate
python fixtures_data.py      # Données de démo
python manage.py runserver
```

## 📚 Documentation API

| URL | Description |
|-----|-------------|
| `/swagger/` | Documentation Swagger interactive |
| `/redoc/` | Documentation ReDoc |
| `/admin/` | Interface d'administration |

## 🔐 Authentification JWT

```bash
POST /api/auth/token/
{"username": "admin", "password": "Admin123!"}
→ Utiliser: Authorization: Bearer <access_token>
```

## 📡 Endpoints

### 🗺️ Zones
| Méthode | URL | Action |
|---------|-----|--------|
| GET/POST | `/api/communes/` | Lister/créer communes |
| GET/POST | `/api/quartiers/` | Lister/créer quartiers |

### 📍 Signalements
| Méthode | URL | Action |
|---------|-----|--------|
| GET/POST | `/api/signalements/` | Lister/créer signalements |
| POST | `/api/signalements/{id}/traiter/` | Changer le statut |
| GET | `/api/signalements/statistiques/` | 📊 Tableau de bord |
| GET | `/api/signalements/carte/` | 🗺️ Données cartographiques |
| GET | `/api/signalements/urgents/` | 🚨 Signalements urgents |

### 🚛 Collectes
| Méthode | URL | Action |
|---------|-----|--------|
| GET/POST | `/api/vehicules/` | Gestion des véhicules |
| GET/POST | `/api/tournees/` | Gestion des tournées |
| POST | `/api/tournees/{id}/demarrer/` | Démarrer une tournée |
| POST | `/api/tournees/{id}/terminer/` | Terminer (résout les signalements) |
| GET | `/api/tournees/planning/` | Planning des tournées à venir |

## 🏗️ Architecture
```
dechets_urbains/
├── config/          # Configuration Django
├── zones/           # Communes et quartiers
├── signalements/    # Signalements citoyens (cœur du système)
├── collectes/       # Véhicules et tournées de collecte
└── media/           # Photos uploadées
```
