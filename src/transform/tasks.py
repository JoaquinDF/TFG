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
                for k, v in Organization._fields.items():
                    if k != 'id' and k in mapper and mapper[k]:
                        tmp = ''
                        if isinstance(mapper[k], str):
                            for field in mapper[k].split(';'):
                                if document[field]:
                                    tmp += document[field] + ';'
                            organization[k] = tmp
                        else:
                            organization[k] = document[mapper[k]]
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
