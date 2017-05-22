from rest_framework import routers

from .views import OrganizationMapperViewSet, OrganizationViewSet


router = routers.DefaultRouter()
router.register(r'organizationMapper', OrganizationMapperViewSet, r'organizationMapper')
router.register(r'organization', OrganizationViewSet, r'organization')

urlpatterns = router.urls
