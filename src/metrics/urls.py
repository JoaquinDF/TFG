from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r'PorcentajeSubvencionado', PorcentajeSubvencionadoViewSet, r'PorcentajeSubvencionado')
urlpatterns = router.urls
