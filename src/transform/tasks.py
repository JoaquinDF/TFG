from __future__ import absolute_import, unicode_literals

from celery import shared_task

from utils.mapper import *
from .models import *


@shared_task
def organization_mapping_task():
    for mapper in OrganizationMapper.objects:
        data_mapping(mapper=mapper, format_class=Organization, data_type='organizations')
        remove_duplicates(mapper=mapper, data_type='organizations')
    return {'name': 'organization_mapping_task', 'finished': True}


@shared_task
def project_mapping_task():
    for mapper in ProjectMapper.objects:
        data_mapping(mapper=mapper, format_class=Project, data_type='projects')
        remove_duplicates(mapper=mapper, data_type='projects')
    return {'name': 'project_mapping_task', 'finished': True}


@shared_task
def call_mapping_task():
    for mapper in CallMapper.objects:
        data_mapping(mapper=mapper, format_class=Call, data_type='calls')
        remove_duplicates(mapper=mapper, data_type='calls')
    return {'name': 'call_mapping_task', 'finished': True}


@shared_task
def thematic_mapping_task():
    for mapper in ThematicMapper.objects:
        data_mapping(mapper=mapper, format_class=Thematic, data_type='thematics')
        remove_duplicates(mapper=mapper, data_type='thematics')
    return {'name': 'thematic_mapping_task', 'finished': True}


@shared_task
def program_mapping_task():
    for mapper in ProgramMapper.objects:
        data_mapping(mapper=mapper, format_class=Program, data_type='programs')
        remove_duplicates(mapper=mapper, data_type='programs')
    return {'name': 'program_mapping_task', 'finished': True}


@shared_task
def person_mapping_task():
    for mapper in PersonMapper.objects:
        data_mapping(mapper=mapper, format_class=Person, data_type='persons')
        remove_duplicates(mapper=mapper, data_type='persons')
    return {'name': 'person_mapping_task', 'finished': True}


@shared_task
def result_mapping_task():
    for mapper in ResultMapper.objects:
        data_mapping(mapper=mapper, format_class=Result, data_type='results')
        remove_duplicates(mapper=mapper, data_type='results')
    return {'name': 'result_mapping_task', 'finished': True}


@shared_task
def project_organization_mapping_task():
    for mapper in ProjectOrganizationMapper.objects:
        data_mapping(mapper=mapper, format_class=ProjectOrganization, data_type='project-organization')
        remove_empty(mapper=mapper, format_class=ProjectOrganization, data_type='project-organization')
    return {'name': 'project_organization_mapping_task', 'finished': True}


@shared_task
def project_call_mapping_task():
    for mapper in ProjectCallMapper.objects:
        data_mapping(mapper=mapper, format_class=ProjectCall, data_type='project-call')
        remove_empty(mapper=mapper, format_class=ProjectCall, data_type='project-call')
    return {'name': 'project_call_mapping_task', 'finished': True}


@shared_task
def call_call_mapping_task():
    for mapper in CallCallMapper.objects:
        data_mapping(mapper=mapper, format_class=CallCall, data_type='call-call')
        remove_empty(mapper=mapper, format_class=CallCall, data_type='call-call')
    return {'name': 'call_call_mapping_task', 'finished': True}


@shared_task
def person_organization_mapping_task():
    for mapper in PersonOrganizationMapper.objects:
        data_mapping(mapper=mapper, format_class=PersonOrganization, data_type='person-organization')
        remove_empty(mapper=mapper, format_class=PersonOrganization, data_type='person-organization')
    return {'name': 'person_organization_mapping_task', 'finished': True}


@shared_task
def project_result_mapping_task():
    for mapper in ProjectResultMapper.objects:
        data_mapping(mapper=mapper, format_class=ProjectResult, data_type='project-result')
        remove_empty(mapper=mapper, format_class=ProjectResult, data_type='project-result')
    return {'name': 'project_result_mapping_task', 'finished': True}

# TODO: Add join task
