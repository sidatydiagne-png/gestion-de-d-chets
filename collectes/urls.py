from rest_framework.routers import DefaultRouter
from .views import VehiculeViewSet, TourneeCollecteViewSet

router = DefaultRouter()
router.register(r'vehicules', VehiculeViewSet)
router.register(r'tournees', TourneeCollecteViewSet)
urlpatterns = router.urls
