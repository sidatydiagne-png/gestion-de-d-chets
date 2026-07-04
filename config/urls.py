from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="API Gestion des Déchets Urbains",
        default_version='v1',
        description="""
Système Intelligent de Gestion des Déchets Urbains 🗑️

Fonctionnalités :
- 📍 Signalement de dépôts sauvages avec photo et géolocalisation
- 🗺️ Cartographie des points noirs par quartier/commune
- 🚛 Planification des tournées de collecte
- 📊 Statistiques et tableau de bord décisionnel
        """,
        contact=openapi.Contact(email="admin@dechets.sn"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    path('', RedirectView.as_view(url='/app/', permanent=False)),
    path('admin/', admin.site.urls),

    # Auth JWT
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API métier
    path('api/', include('zones.urls')),
    path('api/', include('signalements.urls')),
    path('api/', include('collectes.urls')),

    # Documentation Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),

    # Frontend (interface web)
    path('app/', include('frontend.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)