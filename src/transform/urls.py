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

router.register(r'thematic', ThematicViewSet, r'thematic')
router.register(r'thematicMapper', ThematicMapperViewSet, r'thematicMapper')
router.register(r'thematicMapping', ThematicMappingViewSet, r'thematicMapping')

router.register(r'program', ProgramViewSet, r'program')
router.register(r'programMapper', ProgramMapperViewSet, r'programMapper')
router.register(r'programMapping', ProgramMappingViewSet, r'programMapping')

router.register(r'person', PersonViewSet, r'person')
router.register(r'personMapper', PersonMapperViewSet, r'personMapper')
router.register(r'personMapping', PersonMappingViewSet, r'personMapping')

router.register(r'result', ResultViewSet, r'result')
router.register(r'resultMapper', ResultMapperViewSet, r'resultMapper')
router.register(r'resultMapping', ResultMappingViewSet, r'resultMapping')

router.register(r'projectorganization', ProjectOrganizationViewSet, r'projectorganization')
router.register(r'projectorganizationmapper', ProjectOrganizationMapperViewSet, r'projectorganizationmapper')
router.register(r'projectorganizationmapping', ProjectOrganizationMappingViewSet, r'projectorganizationmapping')

router.register(r'projectcall', ProjectCallViewSet, r'projectcall')
router.register(r'projectcallmapper', ProjectCallMapperViewSet, r'projectcallmapper')
router.register(r'projectcallmapping', ProjectCallMappingViewSet, r'projectcallmapping')

router.register(r'callcall', CallCallViewSet, r'callcall')
router.register(r'callcallmapper', CallCallMapperViewSet, r'callcallmapper')
router.register(r'callcallmapping', CallCallMappingViewSet, r'callcallmapping')

router.register(r'callthematic', CallThematicViewSet, r'callthematic')
router.register(r'callthematicmapper', CallThematicMapperViewSet, r'callthematicmapper')
router.register(r'callthematicmapping', CallThematicMappingViewSet, r'callthematicmapping')

router.register(r'personorganization', PersonOrganizationViewSet, r'personorganization')
router.register(r'personorganizationMapper', PersonOrganizationMapperViewSet, r'personorganizationMapper')
router.register(r'personorganizationMapping', PersonOrganizationMappingViewSet, r'personorganizationMapping')

router.register(r'projectresult', ProjectResultViewSet, r'projectresult')
router.register(r'projectresultmapper', ProjectResultMapperViewSet, r'projectresultmapper')
router.register(r'projectresultmapping', ProjectResultMappingViewSet, r'projectresultmapping')

urlpatterns = router.urls
