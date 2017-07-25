from rest_framework import routers

from .views import *


router = routers.DefaultRouter()

router.register(r'projectMapper', ProjectMapperViewSet, r'projectMapper')
router.register(r'projectMapping', ProjectMappingViewSet, r'projectMapping')

router.register(r'callMapper', CallMapperViewSet, r'callMapper')
router.register(r'callMapping', CallMappingViewSet, r'callMapping')

router.register(r'organizationMapper', OrganizationMapperViewSet, r'organizationMapper')
router.register(r'organizationMapping', OrganizationMappingViewSet, r'organizationMapping')

router.register(r'personMapper', PersonMapperViewSet, r'personMapper')
router.register(r'personMapping', PersonMappingViewSet, r'personMapping')

router.register(r'projectcallmapper', ProjectCallMapperViewSet, r'projectcallmapper')
router.register(r'projectcallmapping', ProjectCallMappingViewSet, r'projectcallmapping')

router.register(r'projectorganizationmapper', ProjectOrganizationMapperViewSet, r'projectorganizationmapper')
router.register(r'projectorganizationmapping', ProjectOrganizationMappingViewSet, r'projectorganizationmapping')

router.register(r'personprojectMapper', PersonProjectMapperViewSet, r'personprojectMapper')
router.register(r'personprojectMapping', PersonProjectMappingViewSet, r'personprojectMapping')

router.register(r'personorganizationMapper', PersonOrganizationMapperViewSet, r'personorganizationMapper')
router.register(r'personorganizationMapping', PersonOrganizationMappingViewSet, r'personorganizationMapping')

urlpatterns = router.urls
