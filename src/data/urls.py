from rest_framework import routers

from .views import *


router = routers.DefaultRouter()

router.register(r'project', ProjectViewSet, r'project')
router.register(r'call', CallViewSet, r'call')
router.register(r'organization', OrganizationViewSet, r'organization')
router.register(r'person', PersonViewSet, r'person')
router.register(r'projectcall', ProjectCallViewSet, r'projectcall')
router.register(r'projectorganization', ProjectOrganizationViewSet, r'projectorganization')
router.register(r'personproject', PersonProjectViewSet, r'personproject')
router.register(r'personorganization', PersonOrganizationViewSet, r'personorganization')

urlpatterns = router.urls