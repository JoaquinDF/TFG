from rest_framework import routers

from .views import *

router = routers.DefaultRouter()

router.register(r'projectmapper', ProjectMapperViewSet, r'projectmapper')
router.register(r'projectmapping', ProjectMappingViewSet, r'projectmapping')
router.register(r'deleteprojectmapper', DeleteProjectMapperViewSet, r'deleteprojectmapper')



router.register(r'callmapper', CallMapperViewSet, r'callmapper')
router.register(r'callmapping', CallMappingViewSet, r'callmapping')
router.register(r'deletecallmapper', DeleteCallMapperViewSet, r'deletecallmapper')


router.register(r'organizationmapper', OrganizationMapperViewSet, r'organizationmapper')
router.register(r'organizationmapping', OrganizationMappingViewSet, r'organizationmapping')
router.register(r'deleteorganizationmapper', DeleteOrganizationMapperViewSet, r'deleteorganizationmapper')


router.register(r'personmapper', PersonMapperViewSet, r'personmapper')
router.register(r'personmapping', PersonMappingViewSet, r'personmapping')

router.register(r'projectcallmapper', ProjectCallMapperViewSet, r'projectcallmapper')
router.register(r'projectcallmapping', ProjectCallMappingViewSet, r'projectcallmapping')
router.register(r'deleteprojectcallmapper', DeleteProjectCallMapperViewSet, r'deleteprojectcallmapper')




router.register(r'projectorganizationmapper', ProjectOrganizationMapperViewSet, r'projectorganizationmapper')
router.register(r'projectorganizationmapping', ProjectOrganizationMappingViewSet, r'projectorganizationmapping')
router.register(r'deleteprojectorganizationmapper', DeleteProjectOrganizationMapperViewSet,
                r'deleteprojectorganizationmapper')


router.register(r'personprojectmapper', PersonProjectMapperViewSet, r'personprojectmapper')
router.register(r'personprojectmapping', PersonProjectMappingViewSet, r'personprojectmapping')

router.register(r'personorganizationmapper', PersonOrganizationMapperViewSet, r'personorganizationmapper')
router.register(r'personorganizationmapping', PersonOrganizationMappingViewSet, r'personorganizationmapping')

urlpatterns = router.urls
