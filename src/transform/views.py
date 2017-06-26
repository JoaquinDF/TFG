from rest_framework.viewsets import ViewSet, ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response

from .serializers import *
from .tasks import *


# ORGANIZATION
class OrganizationViewSet(ReadOnlyModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class OrganizationMapperViewSet(ModelViewSet):
    queryset = OrganizationMapper.objects.all()
    serializer_class = OrganizationMapperSerializer


class OrganizationMappingViewSet(ViewSet):
    def create(self, request):
        organization_mapping_task.delay()
        return Response({'data': 'organization', 'queued': True})


# PROJECT
class ProjectViewSet(ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectMapperViewSet(ModelViewSet):
    queryset = ProjectMapper.objects.all()
    serializer_class = ProjectMapperSerializer


class ProjectMappingViewSet(ViewSet):
    def create(self, request):
        project_mapping_task.delay()
        return Response({'data': 'project', 'queued': True})


# CALL
class CallViewSet(ReadOnlyModelViewSet):
    queryset = Call.objects.all()
    serializer_class = CallSerializer


class CallMapperViewSet(ModelViewSet):
    queryset = CallMapper.objects.all()
    serializer_class = CallMapperSerializer


class CallMappingViewSet(ViewSet):
    def create(self, request):
        call_mapping_task.delay()
        return Response({'data': 'call', 'queued': True})


# PROGRAM
class ProgramViewSet(ReadOnlyModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer


class ProgramMapperViewSet(ModelViewSet):
    queryset = ProgramMapper.objects.all()
    serializer_class = ProgramMapperSerializer


class ProgramMappingViewSet(ViewSet):
    def create(self, request):
        program_mapping_task.delay()
        return Response({'data': 'program', 'queued': True})


# PERSON
class PersonViewSet(ReadOnlyModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class PersonMapperViewSet(ModelViewSet):
    queryset = PersonMapper.objects.all()
    serializer_class = PersonMapperSerializer


class PersonMappingViewSet(ViewSet):
    def create(self, request):
        person_mapping_task.delay()
        return Response({'data': 'person', 'queued': True})


# RESULTS
class ResultViewSet(ReadOnlyModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer


class ResultMapperViewSet(ModelViewSet):
    queryset = ResultMapper.objects.all()
    serializer_class = ResultMapperSerializer


class ResultMappingViewSet(ViewSet):
    def create(self, request):
        result_mapping_task.delay()
        return Response({'data': 'result', 'queued': True})


# PROJECT-ORGANIZATION
class ProjectOrganizationViewSet(ReadOnlyModelViewSet):
    queryset = ProjectOrganization.objects.all()
    serializer_class = ProjectOrganizationSerializer


class ProjectOrganizationMapperViewSet(ModelViewSet):
    queryset = ProjectOrganizationMapper.objects.all()
    serializer_class = ProjectOrganizationMapperSerializer


class ProjectOrganizationMappingViewSet(ViewSet):
    def create(self, request):
        project_organization_mapping_task.delay()
        return Response({'data': 'project-organization', 'queued': True})


# PROJECT-CALL
class ProjectCallViewSet(ReadOnlyModelViewSet):
    queryset = ProjectCall.objects.all()
    serializer_class = ProjectCallSerializer


class ProjectCallMapperViewSet(ModelViewSet):
    queryset = ProjectCallMapper.objects.all()
    serializer_class = ProjectCallMapperSerializer


class ProjectCallMappingViewSet(ViewSet):
    def create(self, request):
        project_call_mapping_task.delay()
        return Response({'data': 'project-call', 'queued': True})


# CALL-CALL
class CallCallViewSet(ReadOnlyModelViewSet):
    queryset = CallCall.objects.all()
    serializer_class = CallCallSerializer


class CallCallMapperViewSet(ModelViewSet):
    queryset = CallCallMapper.objects.all()
    serializer_class = CallCallMapperSerializer


class CallCallMappingViewSet(ViewSet):
    def create(self, request):
        call_call_mapping_task.delay()
        return Response({'data': 'call-call', 'queued': True})


# PERSON-ORGANIZATION
class PersonOrganizationViewSet(ReadOnlyModelViewSet):
    queryset = PersonOrganization.objects.all()
    serializer_class = PersonOrganizationSerializer


class PersonOrganizationMapperViewSet(ModelViewSet):
    queryset = PersonOrganizationMapper.objects.all()
    serializer_class = PersonOrganizationMapperSerializer


class PersonOrganizationMappingViewSet(ViewSet):
    def create(self, request):
        person_organization_mapping_task.delay()
        return Response({'data': 'person-organization', 'queued': True})


# PROJECT-RESULT
class ProjectResultViewSet(ReadOnlyModelViewSet):
    queryset = ProjectResult.objects.all()
    serializer_class = ProjectResultSerializer


class ProjectResultMapperViewSet(ModelViewSet):
    queryset = ProjectResultMapper.objects.all()
    serializer_class = ProjectResultMapperSerializer


class ProjectResultMappingViewSet(ViewSet):
    def create(self, request):
        project_result_mapping_task.delay()
        return Response({'data': 'project-result', 'queued': True})
