from rest_framework_mongoengine import serializers

from .models import OrganizationMapper


class OrganizationMapperSerializer(serializers.DocumentSerializer):
    class Meta:
        model = OrganizationMapper
        fields = '__all__'
