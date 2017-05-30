from rest_framework_mongoengine import serializers

from .models import OrganizationMapper, Organization


class OrganizationMapperSerializer(serializers.DocumentSerializer):
    class Meta:
        model = OrganizationMapper
        fields = '__all__'


class OrganizationSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Organization
        fields = '__all__'
