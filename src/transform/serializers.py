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


class PersonMapperSerializer(serializers.DocumentSerializer):
    class Meta:
        model = PersonMapper
        fields = '__all__'


class PersonSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Person
        fields = '__all__'


class ProjectOrganizationMapperSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ProjectOrganizationMapper
        fields = '__all__'


class ProjectOrganizationSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ProjectOrganization
        fields = '__all__'


class ProjectCallMapperSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ProjectCallMapper
        fields = '__all__'


class ProjectCallSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ProjectCall
        fields = '__all__'


class CallCallMapperSerializer(serializers.DocumentSerializer):
    class Meta:
        model = CallCallMapper
        fields = '__all__'


class CallCallSerializer(serializers.DocumentSerializer):
    class Meta:
        model = CallCall
        fields = '__all__'
