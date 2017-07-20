from rest_framework_mongoengine import serializers

from .models import *


class ConvocatoriaSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Convocatoria
        fields = '__all__'


class ConvocatoriaMapperSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ConvocatoriaMapper
        fields = '__all__'


class ProyectoSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Proyecto
        fields = '__all__'


class ProyectoMapperSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ProyectoMapper
        fields = '__all__'


class OrganizacionSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Organizacion
        depth = 2
        fields = '__all__'


class OrganizacionMapperSerializer(serializers.DocumentSerializer):
    class Meta:
        model = OrganizacionMapper
        depth = 2
        fields = '__all__'


class PersonaSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Persona
        fields = '__all__'


class PersonaMapperSerializer(serializers.DocumentSerializer):
    class Meta:
        model = PersonaMapper
        exclude = ('validacion',)


class ProyectoConvocatoriaSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ProyectoConvocatoria
        fields = '__all__'


class ProyectoConvocatoriaMapperSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ProyectoConvocatoriaMapper
        fields = '__all__'


class ProyectoOrganizacionSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ProyectoOrganizacion
        fields = '__all__'


class ProyectoOrganizacionMapperSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ProyectoOrganizacionMapper
        fields = '__all__'


class PersonaProyectoSerializer(serializers.DocumentSerializer):
    class Meta:
        model = PersonaProyecto
        fields = '__all__'


class PersonaProyectoMapperSerializer(serializers.DocumentSerializer):
    class Meta:
        model = PersonaProyectoMapper
        fields = '__all__'


class PersonaOrganizacionSerializer(serializers.DocumentSerializer):
    class Meta:
        model = PersonaOrganizacion
        fields = '__all__'


class PersonaOrganizacionMapperSerializer(serializers.DocumentSerializer):
    class Meta:
        model = PersonaOrganizacionMapper
        fields = '__all__'
