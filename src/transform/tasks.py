from __future__ import absolute_import, unicode_literals

from celery import shared_task

from utils.mapper import data_mapping, remove_duplicates
from .models import *


@shared_task
def organization_mapping_task():
    for mapper in OrganizationMapper.objects:
        data_mapping(mapper=mapper, format_class=Organization, data_type='organizations')
        remove_duplicates(mapper=mapper, data_type='organizations')
    return {'name': 'organization_matching', 'finished': True}


@shared_task
def project_mapping_task():
    for mapper in ProjectMapper.objects:
        data_mapping(mapper=mapper, format_class=Project, data_type='projects')
        remove_duplicates(mapper=mapper, data_type='projects')
    return {'name': 'project_mapping', 'finished': True}


@shared_task
def call_mapping_task():
    for mapper in CallMapper.objects:
        data_mapping(mapper=mapper, format_class=Call, data_type='calls')
        remove_duplicates(mapper=mapper, data_type='calls')
    return {'name': 'call_mapping', 'finished': True}


@shared_task
def person_mapping_task():
    for mapper in PersonMapper.objects:
        data_mapping(mapper=mapper, format_class=Person, data_type='persons')
        remove_duplicates(mapper=mapper, data_type='persons')
    return {'name': 'person_mapping', 'finished': True}


@shared_task
def project_organization_mapping_task():
    for mapper in ProjectOrganizationMapper.objects:
        data_mapping(mapper=mapper, format_class=ProjectOrganization, data_type='project-organization')
    return {'name': 'project_organization_mapping_task', 'finished': True}


@shared_task
def project_call_mapping_task():
    for mapper in ProjectCallMapper.objects:
        data_mapping(mapper=mapper, format_class=ProjectCall, data_type='project-call')
    return {'name': 'project_call_mapping_task', 'finished': True}


@shared_task
def call_call_mapping_task():
    for mapper in CallCallMapper.objects:
        data_mapping(mapper=mapper, format_class=CallCall, data_type='call-call')
    return {'name': 'call_call_mapping_task', 'finished': True}


# TODO: Add join task
