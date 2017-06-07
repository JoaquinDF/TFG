from __future__ import absolute_import, unicode_literals

import logging
from celery import shared_task
from pymongo.bulk import BulkWriteError

from utils.mongodb import Mongodb
from .models import OrganizationMapper, Organization


@shared_task
def organization_mapping_task():
    with Mongodb() as mongodb:
        db = mongodb.db
        for mapper in OrganizationMapper.objects:
            bulk = db['structured.' + mapper.collection].initialize_ordered_bulk_op()
            collection = db.get_collection(mapper.collection)
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
                            organization[k] = tmp.rstrip(';')
                        else:
                            organization[k] = document[mapper[k]]
                bulk.find({'_id': organization.id}).upsert().replace_one(organization.to_mongo())
            try:
                bulk.execute()
            except BulkWriteError as bwe:
                logging.debug(bwe.details)
    return {'name': 'organization_matching', 'finished': True}
