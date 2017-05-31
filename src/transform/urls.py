from rest_framework import routers

from .views import OrganizationViewSet, OrganizationMapperViewSet, OrganizationMappingViewSet


router = routers.DefaultRouter()
router.register(r'organization', OrganizationViewSet, r'organization')
router.register(r'organizationMapper', OrganizationMapperViewSet, r'organizationMapper')
router.register(r'organizationMapping', OrganizationMappingViewSet, r'organizationMapping')

urlpatterns = router.urls
