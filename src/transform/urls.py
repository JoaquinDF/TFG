from rest_framework import routers

from .views import *


router = routers.DefaultRouter()
router.register(r'organization', OrganizationViewSet, r'organization')
router.register(r'organizationMapper', OrganizationMapperViewSet, r'organizationMapper')
router.register(r'organizationMapping', OrganizationMappingViewSet, r'organizationMapping')
router.register(r'project', ProjectViewSet, r'project')
router.register(r'projectMapper', ProjectMapperViewSet, r'projectMapper')
router.register(r'projectMapping', ProjectMappingViewSet, r'projectMapping')
router.register(r'call', CallViewSet, r'call')
router.register(r'callMapper', CallMapperViewSet, r'callMapper')
router.register(r'callMapping', CallMappingViewSet, r'callMapping')

urlpatterns = router.urls
