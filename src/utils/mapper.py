import logging
from pymongo.errors import BulkWriteError, InvalidOperation

from utils.mongodb import Mongodb


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


def data_mapping(mapper, format_class, data_type):
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


def remove_duplicates(mapper, data_type):
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
