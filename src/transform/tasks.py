from __future__ import absolute_import, unicode_literals

import difflib
from celery import shared_task

from utils.mongodb import Mongodb
from .models import OrganizationMapper, Organization


@shared_task
def organization_mapping_task():
    for mapper in OrganizationMapper.objects:
        with Mongodb() as mongodb:
            db = mongodb.db
            collection = db.get_collection(mapper.collection)
            bulk = Organization._get_collection().initialize_ordered_bulk_op()
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
                bulk.find({'_id': organization.id}).upsert().replace_one(organization.to_mongo())
            bulk.execute()
    return {'name': 'organization_matching', 'finished': True}


@shared_task
def organization_find_task(field, key, limit):
    results = []
    for organization in Organization.objects:
        if field in organization:
            l = []
            for s in organization[field].split(' '):
                seq = difflib.SequenceMatcher(lambda x: x in " \t", key, s)
                l.append(seq.ratio())
            results.append({
                'id': str(organization.id),
                field: organization[field],
                'ratio': str(max(l))
            })
    return sorted(results, key=lambda x: x['ratio'], reverse=True)[:limit]
