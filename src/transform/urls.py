from rest_framework import routers

from .views import OrganizationViewSet


router = routers.DefaultRouter()
router.register(r'organization', OrganizationViewSet, r'organization')

urlpatterns = router.urls
