from rest_framework.routers import DefaultRouter
from .views import CommuneViewSet, QuartierViewSet

router = DefaultRouter()
router.register(r'communes', CommuneViewSet)
router.register(r'quartiers', QuartierViewSet)
urlpatterns = router.urls
