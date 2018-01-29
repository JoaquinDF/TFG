from rest_framework_mongoengine import serializers

from .models import *


class ConvocatoriaSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Convocatoria
        fields = '__all__'


class ProyectoSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Proyecto
        fields = '__all__'


class OrganizacionSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Organizacion
        depth = 2
        fields = '__all__'


class PersonaSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Persona
        fields = '__all__'


class CommunitySerializer(serializers.DocumentSerializer):
    class Meta:
        model = Community
        fields = '__all__'


class ProyectoConvocatoriaSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ProyectoConvocatoria
        fields = '__all__'


class ProyectoOrganizacionSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ProyectoOrganizacion
        fields = '__all__'


class PersonaProyectoSerializer(serializers.DocumentSerializer):
    class Meta:
        model = PersonaProyecto
        fields = '__all__'


class PersonaOrganizacionSerializer(serializers.DocumentSerializer):
    class Meta:
        model = PersonaOrganizacion
        fields = '__all__'


class OrganizationMetricSerializer(serializers.DocumentSerializer):
    class Meta:
        model = OrganizationMetric
        fields = '__all__'


class RegionMetricSerializer(serializers.DocumentSerializer):
    class Meta:
        model = RegionMetric
        fields = '__all__'


class OrganizationMetricSerializer(serializers.DocumentSerializer):
    class Meta:
        model = OrganizationMetric
        fields = '__all__'
