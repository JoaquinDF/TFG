from __future__ import absolute_import, unicode_literals
from celery import shared_task

from utils.mongodb import Mongodb
from .models import OrganizationMapper, Organization


@shared_task
def organization_task():
    for mapper in OrganizationMapper.objects:
        with Mongodb() as mongodb:
            db = mongodb.db
            collection = db.get_collection(mapper.collection)
            for document in collection.find({}):
                organization = Organization()
                organization.id = document['_id']
                if mapper.key:
                    organization.key = document[mapper.key]
                if mapper.name:
                    organization.name = document[mapper.name]
                if mapper.activity_type:
                    organization.activity_type = document[mapper.activity_type]
                if mapper.address:
                    tmp = ''
                    for address in mapper.address.split(';'):
                        if document[address]:
                            tmp = tmp + document[address] + '\n'
                    organization.address = tmp
                if mapper.country:
                    organization.country = document[mapper.country]
                if mapper.telephone:
                    organization.telephone = document[mapper.telephone]
                if mapper.www:
                    organization.www = document[mapper.www]
                organization.save()
