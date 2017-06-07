from rest_framework_mongoengine import serializers

from .models import *


class OrganizationMapperSerializer(serializers.DocumentSerializer):
    class Meta:
        model = OrganizationMapper
        fields = '__all__'


class OrganizationSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class ProjectMapperSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ProjectMapper
        fields = '__all__'


class ProjectSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class CallMapperSerializer(serializers.DocumentSerializer):
    class Meta:
        model = CallMapper
        fields = '__all__'


class CallSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Call
        fields = '__all__'
