from __future__ import absolute_import, unicode_literals

from celery import shared_task

from utils.mapper import *
from .models import *
from data.models import *


@shared_task
def call_mapping_task():
    for mapper in ConvocatoriaMapper.objects:
        data_mapping(mapper=mapper, template=Convocatoria, data_type='calls')
        remove_duplicates(mapper=mapper, data_type='calls')
    return {'name': 'call_mapping_task', 'finished': True}


@shared_task
def project_mapping_task():
    for mapper in ProyectoMapper.objects:
        data_mapping(mapper=mapper, template=Proyecto, data_type='projects')
        remove_duplicates(mapper=mapper, data_type='projects')
    return {'name': 'project_mapping_task', 'finished': True}


@shared_task
def organization_mapping_task():
    for mapper in OrganizacionMapper.objects:
        data_mapping(mapper=mapper, template=Organizacion, data_type='organizations')
        remove_duplicates(mapper=mapper, data_type='organizations')
    return {'name': 'organization_mapping_task', 'finished': True}


@shared_task
def person_mapping_task():
    for mapper in PersonaMapper.objects:
        data_mapping(mapper=mapper, template=Persona, data_type='persons')
        remove_duplicates(mapper=mapper, data_type='persons')
    return {'name': 'person_mapping_task', 'finished': True}


@shared_task
def project_call_mapping_task():
    for mapper in ProyectoConvocatoriaMapper.objects:
        data_mapping(mapper=mapper, template=ProyectoConvocatoria, data_type='project-call')
        # remove_empty(mapper=mapper, format_class=ProyectoConvocatoria, data_type='project-call')
    return {'name': 'project_call_mapping_task', 'finished': True}


@shared_task
def project_organization_mapping_task():
    for mapper in ProyectoOrganizacionMapper.objects:
        data_mapping(mapper=mapper, template=ProyectoOrganizacion, data_type='project-organization')
        # remove_empty(mapper=mapper, format_class=ProyectoOrganizacion, data_type='project-organization')
    return {'name': 'project_organization_mapping_task', 'finished': True}


@shared_task
def person_project_mapping_task():
    for mapper in PersonaProyectoMapper.objects:
        data_mapping(mapper=mapper, template=PersonaProyecto, data_type='person-project')
        remove_empty(mapper=mapper, format_class=PersonaProyecto, data_type='person-project')
    return {'name': 'person_project_mapping_task', 'finished': True}


@shared_task
def person_organization_mapping_task():
    for mapper in PersonaOrganizacionMapper.objects:
        data_mapping(mapper=mapper, template=PersonaOrganizacion, data_type='person-organization')
        remove_empty(mapper=mapper, format_class=PersonaOrganizacion, data_type='person-organization')
    return {'name': 'person_organization_mapping_task', 'finished': True}

# TODO: Add remove duplicates
