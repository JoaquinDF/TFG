from __future__ import absolute_import, unicode_literals

import logging
from celery import shared_task
from pymongo.errors import BulkWriteError, InvalidOperation

from utils.mongodb import Mongodb
from .models import *


# TODO: Add iterate over collections
def __get_nested_docs__(field, doc):
    lst = field.split('.')
    tmp = doc
    for item in lst:
        if item in tmp:
            tmp = tmp[item]
        else:
            tmp = None
            break
    return tmp


def __data_mapping__(mapper, format_class, data_type):
    with Mongodb() as mongodb:
        db = mongodb.db
        bulk = db['structured.{}.{}'.format(data_type, mapper.collection)].initialize_ordered_bulk_op()
        for original in db[mapper.collection].find({}):
            copy = format_class()
            keys = format_class._fields.items()
            copy.id = original['_id']
            for k, v in keys:
                if k != 'id' and k in mapper and mapper[k]:
                    tmp = ''
                    if isinstance(mapper[k], str):
                        for field in mapper[k].split(';'):
                            item = __get_nested_docs__(field, original)
                            if item:
                                tmp += '{};'.format(item)
                        copy[k] = tmp.rstrip(';').upper().encode('utf-8')
                    elif mapper[k] in original and original[mapper[k]]:
                        copy[k] = original[mapper[k]]
            bulk.find({'_id': copy.id}).upsert().replace_one(copy.to_mongo())
        try:
            bulk.execute()
        except BulkWriteError as e:
            logging.debug(e.details)
        except InvalidOperation as e:
            logging.debug(e)


def __remove_duplicates__(mapper, data_type):
    with Mongodb() as mongodb:
        db = mongodb.db
        collection = db['structured.{}.{}'.format(data_type, mapper.collection)]
        bulk = collection.initialize_ordered_bulk_op()
        for key in mapper.key.split(';'):
            cursor = collection.aggregate(
                [
                    {"$group": {"_id": '${}'.format(key), "unique_ids": {"$addToSet": "$_id"}, "count": {"$sum": 1}}},
                    {"$match": {"count": {"$gte": 2}}}
                ]
            )
            response = []
            for doc in cursor:
                del doc["unique_ids"][0]
                for k in doc["unique_ids"]:
                    response.append(k)
            bulk.find({"_id": {"$in": response}}).remove()
        try:
            bulk.execute()
        except BulkWriteError as e:
            logging.debug(e.details)
        except InvalidOperation as e:
            logging.debug(e)


@shared_task
def organization_mapping_task():
    for mapper in OrganizationMapper.objects:
        __data_mapping__(mapper=mapper, format_class=Organization, data_type='organizations')
        __remove_duplicates__(mapper=mapper, data_type='organizations')
    return {'name': 'organization_matching', 'finished': True}


@shared_task
def project_mapping_task():
    for mapper in ProjectMapper.objects:
        __data_mapping__(mapper=mapper, format_class=Project, data_type='projects')
        __remove_duplicates__(mapper=mapper, data_type='projects')
    return {'name': 'project_mapping', 'finished': True}


@shared_task
def call_mapping_task():
    for mapper in CallMapper.objects:
        __data_mapping__(mapper=mapper, format_class=Call, data_type='calls')
        __remove_duplicates__(mapper=mapper, data_type='calls')
    return {'name': 'call_mapping', 'finished': True}


@shared_task
def project_organization_mapping_task():
    for mapper in ProjectOrganizationMapper.objects:
        __data_mapping__(mapper=mapper, format_class=ProjectOrganization, data_type='project-organization')
    return {'name': 'project_organization_mapping_task', 'finished': True}


@shared_task
def project_call_mapping_task():
    for mapper in ProjectCallMapper.objects:
        __data_mapping__(mapper=mapper, format_class=ProjectCall, data_type='project-call')
    return {'name': 'project_call_mapping_task', 'finished': True}


@shared_task
def call_call_mapping_task():
    for mapper in CallCallMapper.objects:
        __data_mapping__(mapper=mapper, format_class=CallCall, data_type='call-call')
    return {'name': 'call_call_mapping_task', 'finished': True}


# TODO: Add join task
