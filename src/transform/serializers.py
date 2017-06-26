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


class ProgramMapperSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ProgramMapper
        fields = '__all__'


class ProgramSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Program
        fields = '__all__'


class PersonMapperSerializer(serializers.DocumentSerializer):
    class Meta:
        model = PersonMapper
        fields = '__all__'


class PersonSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Person
        fields = '__all__'


class ResultMapperSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ResultMapper
        fields = '__all__'


class ResultSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Result
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


class PersonOrganizationMapperSerializer(serializers.DocumentSerializer):
    class Meta:
        model = PersonOrganizationMapper
        fields = '__all__'


class PersonOrganizationSerializer(serializers.DocumentSerializer):
    class Meta:
        model = PersonOrganization
        fields = '__all__'


class ProjectResultMapperSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ProjectResultMapper
        fields = '__all__'


class ProjectResultSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ProjectResult
        fields = '__all__'
