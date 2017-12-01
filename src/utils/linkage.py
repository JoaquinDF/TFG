import logging
import pandas as pd
import recordlinkage as rl

from pymongo.errors import BulkWriteError
from recordlinkage.standardise import clean, phonenumbers

from utils.mongodb import Mongodb


# TODO: Fix deprecated method
def duplicate_collection(df, db, coll):
    del df['_id']
    cursor = db[coll]
    cursor.delete_many({})
    bulk = cursor.initialize_ordered_bulk_op()
    for _, row in df.iterrows():
        bulk.insert(row.to_dict())
    try:
        bulk.execute()
    except BulkWriteError as bwe:
        logging.error(bwe.details)


def save_docs(df, dfa, dfb, db, coll):
    # del dfA['_id']
    # del dfB['_id']
    docs = []
    x_set = set()
    y_set = set()
    for x, y in set(df.index):
        x_set.add(x)
        y_set.add(y)
    for i, row in dfa.iterrows():
        if i not in x_set:
            docs.append(row.to_dict())
    for i, row in dfb.iterrows():
        if i not in y_set:
            docs.append(row.to_dict())
    x_index = set([x[0] for x in set(df.index)])
    y_index = set([y[1] for y in set(df.index)])
    for x, y in set(df.index):
        if x not in x_index or y not in y_index:
            continue
        x_dict = dfa.loc[x].to_dict()
        y_dict = dfb.loc[y].to_dict()
        for key in y_dict.keys():
            if key not in x_set:
                x_dict[key] = y_dict[key]
        docs.append(x_dict)
        x_index.discard(x)
        y_index.discard(y)
    cursor = db[coll]
    cursor.delete_many({})
    bulk = cursor.initialize_ordered_bulk_op()
    for doc in docs:
        bulk.insert(doc)
    try:
        bulk.execute()
    except BulkWriteError as bwe:
        logging.error(bwe.details)


def linkage_two_data(c_structured, c_data, s_key, s_columns):
    with Mongodb() as mongodb:
        db = mongodb.db
        collections = [col for col in db.collection_names() if col.startswith(c_structured)]
        for collection in collections:
            dfs = pd.DataFrame(list(db[collection].find({})))
            d_columns = ['c{}'.format(x['column']) for x in s_columns]
            for i, x in enumerate(s_columns):
                if x['type'] is 'string':
                    dfs[d_columns[i]] = clean(clean(clean(dfs[x['column']],
                                                              strip_accents='unicode'),
                                                        replace_by_none=' '),
                                                  replace_by_none=x['regex'])
                elif x['type'] is 'phonenumber':
                    dfs[d_columns[i]] = phonenumbers(dfs[x['column']])
                else:
                    dfs[d_columns[i]] = dfs[x['column']]
            if db[c_data].count() == 0:
                for column in d_columns:
                    del dfs[column]
                duplicate_collection(dfs, db, c_data)
            else:
                dfd = pd.DataFrame(list(db[c_data].find({})))
                for i, x in enumerate(s_columns):
                    if x['type'] is 'string':
                        dfd[d_columns[i]] = clean(clean(clean(dfd[x['column']],
                                                              strip_accents='unicode'),
                                                        replace_by_none=' '),
                                                  replace_by_none=x['regex'])
                    elif x['type'] is 'phonenumber':
                        dfd[d_columns[i]] = phonenumbers(dfd[x['column']])
                    else:
                        dfd[d_columns[i]] = dfd[x['column']]
                indexer = rl.SortedNeighbourhoodIndex(on='c{}'.format(s_key), window=9)
                pairs = indexer.index(dfs, dfd)
                compare_cl = rl.Compare(pairs, dfs, dfd, low_memory=True)
                for i, column in enumerate(d_columns):
                    compare_cl.exact(column, column, s_columns[i]['column'])
                df = compare_cl.vectors[compare_cl.vectors.sum(axis=1) >= 1]
                for column in d_columns:
                    del dfs[column]
                    del dfd[column]
                save_docs(df, dfs, dfd, db, c_data)
