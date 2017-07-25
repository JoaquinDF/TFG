from rest_framework_mongoengine import serializers

from .models import *


class ConvocatoriaMapperSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ConvocatoriaMapper
        fields = '__all__'


class ProyectoMapperSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ProyectoMapper
        fields = '__all__'


class OrganizacionMapperSerializer(serializers.DocumentSerializer):
    class Meta:
        model = OrganizacionMapper
        depth = 2
        fields = '__all__'


class PersonaMapperSerializer(serializers.DocumentSerializer):
    class Meta:
        model = PersonaMapper
        exclude = ('validacion',)


class ProyectoConvocatoriaMapperSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ProyectoConvocatoriaMapper
        fields = '__all__'


class ProyectoOrganizacionMapperSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ProyectoOrganizacionMapper
        fields = '__all__'


class PersonaProyectoMapperSerializer(serializers.DocumentSerializer):
    class Meta:
        model = PersonaProyectoMapper
        fields = '__all__'


class PersonaOrganizacionMapperSerializer(serializers.DocumentSerializer):
    class Meta:
        model = PersonaOrganizacionMapper
        fields = '__all__'
