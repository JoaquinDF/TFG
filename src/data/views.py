from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializers import *


# CALL
class CallViewSet(ReadOnlyModelViewSet):
    queryset = Convocatoria.objects.all()
    serializer_class = ConvocatoriaSerializer


# PROJECT
class ProjectViewSet(ReadOnlyModelViewSet):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer


# ORGANIZATION
class OrganizationViewSet(ReadOnlyModelViewSet):
    queryset = Organizacion.objects.all()
    serializer_class = OrganizacionSerializer


# PERSON
class PersonViewSet(ReadOnlyModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer


# PROJECT-CALL
class ProjectCallViewSet(ReadOnlyModelViewSet):
    queryset = ProyectoConvocatoria.objects.all()
    serializer_class = ProyectoConvocatoriaSerializer


# PROJECT-ORGANIZATION
class ProjectOrganizationViewSet(ReadOnlyModelViewSet):
    queryset = ProyectoOrganizacion.objects.all()
    serializer_class = ProyectoOrganizacionSerializer


# PERSON-PROJECT
class PersonProjectViewSet(ReadOnlyModelViewSet):
    queryset = PersonaProyecto.objects.all()
    serializer_class = PersonaProyectoSerializer


# PERSON-ORGANIZATION
class PersonOrganizationViewSet(ReadOnlyModelViewSet):
    queryset = PersonaOrganizacion.objects.all()
    serializer_class = PersonaOrganizacionSerializer
