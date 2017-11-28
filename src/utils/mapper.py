from pymongo.operations import DeleteMany, ReplaceOne
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
        if mapper[k] is None:
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
        collection = 'structured.{}.{}'.format(data_type, mapper.collection)
        c = db[collection]
        c.delete_many({})
        requests = []
        for original in db[mapper.collection].find({}):
            copy = copy_object(original, template, mapper)
            requests.append(ReplaceOne(filter={'_id': copy.id}, replacement=copy.to_mongo(), upsert=True))
        mongodb.do_bulk_requests(requests,collection=collection)

def remove_duplicates(mapper, data_type):
    with Mongodb() as mongodb:
        db = mongodb.db
        collection = 'structured.{}.{}'.format(data_type, mapper.collection)
        c = db[collection]
        keys = {}
        for key in mapper.key.split(';'):
            keys[key] = '${}'.format(key)
        cursor = c.aggregate(
            [
                {"$group": {"_id": keys, "unique_ids": {"$addToSet": "$_id"}, "count": {"$sum": 1}}},
                {"$match": {"count": {"$gte": 2}}}
            ]
        )
        requests = []
        response = []
        for doc in cursor:
            del doc["unique_ids"][0]
            for k in doc["unique_ids"]:
                response.append(k)
        requests.append(DeleteMany({"_id": {"$in": response}}))
        mongodb.do_bulk_requests(requests, collection=collection)


def remove_empty(mapper, format_class, data_type):
    with Mongodb() as mongodb:
        collection = 'structured.{}.{}'.format(data_type, mapper.collection)
        requests = []
        keys = format_class._fields.items()
        for k, v in keys:
            if k != 'id':
                requests.append(DeleteMany({k: ""}))
        mongodb.do_bulk_requests(requests, collection=collection)

# TODO: Add iterate over collections
# TODO: Delete duplicates
