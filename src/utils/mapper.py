import logging
from pymongo.errors import BulkWriteError, InvalidOperation
from mongoengine.fields import *

from utils.mongodb import Mongodb


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


def __float_formatter__(string):
    s = string.replace(' ', '').replace('€', '').replace(',', '.')
    l = s.split('.')
    n = ''
    if len(l) > 1:
        for i, j in enumerate(l):
            if i + 1 == len(l):
                n = n + '.' + j
            else:
                n = n + j
    try:
        result = float(n)
    except ValueError:
        result = None
    return result


def copy_object(original, template, mapper):
    copy = template()
    copy.id = original['_id']
    for k, v in template._fields.items():
        if not mapper[k]:
            continue
        elif isinstance(v, StringField):
            tmp = ''
            for field in mapper[k].split(';'):
                item = __get_nested_docs__(field, original)
                if item:
                    tmp += '{};'.format(item)
            copy[k] = tmp.rstrip(';').upper().encode('utf-8')
        elif isinstance(v, FloatField):
            item = __get_nested_docs__(mapper[k], original)
            if isinstance(item, float):
                copy[k] = item
            elif isinstance(item, str):
                copy[k] = __float_formatter__(item)
            else:
                copy[k] = item
        elif isinstance(v, DateTimeField):
            pass
        elif isinstance(v, ListField):
            for field in mapper[k].split(';'):
                item = __get_nested_docs__(field, original)
                copy[k].append(item)
        elif isinstance(v, EmbeddedDocumentField):
            doc = v.document_type
            copy[k] = copy_object(original, doc, mapper[k])
    return copy


def data_mapping(mapper, template, data_type):
    with Mongodb() as mongodb:
        db = mongodb.db
        col = db['structured.{}.{}'.format(data_type, mapper.collection)]
        col.delete_many({})
        bulk = col.initialize_ordered_bulk_op()
        for original in db[mapper.collection].find({}):
            copy = copy_object(original, template, mapper)
            bulk.find({'_id': copy.id}).upsert().replace_one(copy.to_mongo())
        try:
            bulk.execute()
        except BulkWriteError as e:
            logging.debug(e.details)
        except InvalidOperation as e:
            logging.debug(e)


def remove_duplicates(mapper, data_type):
    with Mongodb() as mongodb:
        db = mongodb.db
        collection = db['structured.{}.{}'.format(data_type, mapper.collection)]
        bulk = collection.initialize_ordered_bulk_op()
        keys = {}
        for key in mapper.key.split(';'):
            keys[key] = '${}'.format(key)
        cursor = collection.aggregate(
            [
                {"$group": {"_id": keys, "unique_ids": {"$addToSet": "$_id"}, "count": {"$sum": 1}}},
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


def remove_empty(mapper, format_class, data_type):
    with Mongodb() as mongodb:
        db = mongodb.db
        collection = db['structured.{}.{}'.format(data_type, mapper.collection)]
        bulk = collection.initialize_ordered_bulk_op()
        keys = format_class._fields.items()
        for k, v in keys:
            if k != 'id':
                bulk.find({k: ""}).remove()
        try:
            bulk.execute()
        except BulkWriteError as e:
            logging.debug(e.details)
        except InvalidOperation as e:
            logging.debug(e)

# TODO: Add iterate over collections
# TODO: Delete duplicates
# TODO: Fix deprecated initialize_ordered_bulk_op method
