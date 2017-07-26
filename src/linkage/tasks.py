from __future__ import absolute_import, unicode_literals

import logging
import pandas as pd
import recordlinkage as rl

from celery import shared_task
from pymongo.errors import BulkWriteError
from recordlinkage.standardise import clean, phonenumbers

from utils.mongodb import Mongodb


def duplicate_collection(dfA, db, coll):
    del dfA['_id']
    cursor = db[coll]
    cursor.delete_many({})
    bulk = cursor.initialize_ordered_bulk_op()
    for _, row in dfA.iterrows():
        bulk.insert(row.to_dict())
    try:
        bulk.execute()
    except BulkWriteError as bwe:
        logging.error(bwe.details)


def save_docs(df, dfA, dfB, db, coll):
    # del dfA['_id']
    # del dfB['_id']
    docs = []
    X = set()
    Y = set()
    for x, y in set(df.index):
        X.add(x)
        Y.add(y)
    for i, row in dfA.iterrows():
        if i not in X:
            docs.append(row.to_dict())
    for i, row in dfB.iterrows():
        if i not in Y:
            docs.append(row.to_dict())
    xindex = set([x[0] for x in set(df.index)])
    yindex = set([y[1] for y in set(df.index)])
    for x, y in set(df.index):
        if x not in xindex or y not in yindex:
            continue
        Xdict = dfA.loc[x].to_dict()
        Ydict = dfB.loc[y].to_dict()
        for key in Ydict.keys():
            if key not in X:
                Xdict[key] = Ydict[key]
        docs.append(Xdict)
        xindex.discard(x)
        yindex.discard(y)
    cursor = db[coll]
    cursor.delete_many({})
    bulk = cursor.initialize_ordered_bulk_op()
    for doc in docs:
        bulk.insert(doc)
    try:
        bulk.execute()
    except BulkWriteError as bwe:
        logging.error(bwe.details)


@shared_task
def call_linkage_task():
    logging.info('calls_linkage_task: started')
    with Mongodb() as mongodb:
        db = mongodb.db
        cols = [col for col in db.collection_names() if col.startswith('structured.calls.')]
        for col in cols:
            c = db[col]
            cursor = c.find({})
            dfA = pd.DataFrame(list(cursor))
            dfA['ctituloConvocatoria'] = clean(clean(dfA['tituloConvocatoria'], strip_accents='unicode'), replace_by_none=' ')
            collection = db['data.calls']
            cursor = collection.find({})
            if collection.count() == 0:
                del dfA['ctituloConvocatoria']
                duplicate_collection(dfA, db, 'data.calls')
            else:
                dfB = pd.DataFrame(list(cursor))
                dfB['ctituloConvocatoria'] = clean(clean(dfB['tituloConvocatoria'], strip_accents='unicode'), replace_by_none=' ')
                indexer = rl.SortedNeighbourhoodIndex(on='ctituloConvocatoria', window=9)
                pairs = indexer.index(dfA, dfB)
                compare_cl = rl.Compare(pairs, dfA, dfB, low_memory=True)
                # compare_cl.string('ctituloConvocatoria','ctituloConvocatoria', 'damerau_levenshtein', threshold=.9, name='tituloConvocatoria')
                compare_cl.exact('ctituloConvocatoria', 'ctituloConvocatoria', name='tituloConvocatoria')
                df = compare_cl.vectors[compare_cl.vectors.sum(axis=1) >= 1]
                del dfA['ctituloConvocatoria']
                del dfB['ctituloConvocatoria']
                save_docs(df, dfA, dfB, db, 'data.calls')
    return {'name': 'calls_linkage_task', 'finished': True}


@shared_task
def organization_linkage_task():
    logging.info('organization_linkage_task: started')
    with Mongodb() as mongodb:
        db = mongodb.db
        cols = [col for col in db.collection_names() if col.startswith('structured.organizations.')]
        for col in cols:
            c = db[col]
            cursor = c.find({})
            dfA = pd.DataFrame(list(cursor))
            dfA['cnombre'] = clean(clean(clean(dfA['nombre'], strip_accents='unicode', replace_by_none='.'), replace_by_none=r'\b(sa|sl| )\b'))
            c = db['data.organizations']
            cursor = c.find({})
            if c.count() == 0:
                del dfA['cnombre']
                duplicate_collection(dfA, db, 'data.organizations')
            else:
                dfB = pd.DataFrame(list(cursor))
                dfB['cnombre'] = clean(clean(clean(dfB['nombre'], strip_accents='unicode', replace_by_none='.'), replace_by_none=r'\b(sa|sl| )\b'))
                indexer = rl.SortedNeighbourhoodIndex(on='cnombre', window=9)
                pairs = indexer.index(dfA, dfB)
                compare_cl = rl.Compare(pairs, dfA, dfB, low_memory=True)
                # compare_cl.string('cnombre','cnombre', 'damerau_levenshtein', threshold=.9, name='nombre')
                compare_cl.exact('cnombre', 'cnombre', name='nombre')
                df = compare_cl.vectors[compare_cl.vectors.sum(axis=1) >= 1]
                del dfA['cnombre']
                del dfB['cnombre']
                save_docs(df, dfA, dfB, db, 'data.organizations')
    return {'name': 'organization_linkage_task', 'finished': True}


@shared_task
def project_linkage_task():
    logging.info('project_linkage_task: started')
    with Mongodb() as mongodb:
        db = mongodb.db
        cols = [col for col in db.collection_names() if col.startswith('structured.projects.')]
        for col in cols:
            c = db[col]
            cursor = c.find({})
            dfA = pd.DataFrame(list(cursor))
            dfA['ctituloProyecto'] = clean(clean(dfA['tituloProyecto'], strip_accents='unicode'), replace_by_none=' ')
            c = db['data.projects']
            cursor = c.find({})
            if c.count() == 0:
                del dfA['ctituloProyecto']
                duplicate_collection(dfA, db, 'data.projects')
            else:
                dfB = pd.DataFrame(list(cursor))
                dfB['ctituloProyecto'] = clean(clean(dfB['tituloProyecto'], strip_accents='unicode'), replace_by_none=' ')
                indexer = rl.SortedNeighbourhoodIndex(on='ctituloProyecto', window=9)
                pairs = indexer.index(dfA, dfB)
                compare_cl = rl.Compare(pairs, dfA, dfB, low_memory=True)
                # compare_cl.string('ctituloProyecto','ctituloProyecto', 'damerau_levenshtein', threshold=.9, name='tituloProyecto')
                compare_cl.exact('ctituloProyecto', 'ctituloProyecto', name='tituloProyecto')
                df = compare_cl.vectors[compare_cl.vectors.sum(axis=1) >= 1]
                del dfA['ctituloProyecto']
                del dfB['ctituloProyecto']
                save_docs(df, dfA, dfB, db, 'data.projects')
    return {'name': 'project_linkage_task', 'finished': True}


@shared_task
def person_linkage_task():
    logging.info('person_linkage_task: started')
    with Mongodb() as mongodb:
        db = mongodb.db
        cols = [col for col in db.collection_names() if col.startswith('structured.persons.')]
        for col in cols:
            c = db[col]
            cursor = c.find({})
            dfA = pd.DataFrame(list(cursor))
            dfA['cnombre'] = clean(clean(dfA['nombre'], strip_accents='unicode'), replace_by_none=' ')
            dfA['capellidos'] = clean(clean(dfA['apellidos'], strip_accents='unicode'), replace_by_none=' ')
            dfA['ctelefono'] = phonenumbers(dfA['telefono'])
            c = db['data.persons']
            cursor = c.find({})
            if c.count() == 0:
                del dfA['cnombre']
                del dfA['capellidos']
                del dfA['ctelefono']
                duplicate_collection(dfA, db, 'data.persons')
            else:
                dfB = pd.DataFrame(list(cursor))
                dfB['cnombre'] = clean(clean(dfB['nombre'], strip_accents='unicode'), replace_by_none=' ')
                dfB['capellidos'] = clean(clean(dfB['apellidos'], strip_accents='unicode'), replace_by_none=' ')
                dfB['ctelefono'] = phonenumbers(dfB['telefono'])
                indexer = rl.SortedNeighbourhoodIndex(on='ctelefono', window=9)
                pairs = indexer.index(dfA, dfB)
                compare_cl = rl.Compare(pairs, dfA, dfB, low_memory=True)
                # compare_cl.string('cnombre','cnombre', 'damerau_levenshtein', threshold=.9, name='nombre')
                compare_cl.exact('cnombre', 'cnombre', name='nombre')
                # compare_cl.string('cnombre','cnombre', 'damerau_levenshtein', threshold=.9, name='nombre')
                compare_cl.exact('capellidos', 'capellidos', name='apellidos')
                # compare_cl.string('cnombre','cnombre', 'damerau_levenshtein', threshold=.9, name='nombre')
                compare_cl.exact('ctelefono', 'ctelefono', name='telefono')
                df = compare_cl.vectors[compare_cl.vectors.sum(axis=1) >= 1]
                del dfA['cnombre']
                del dfB['cnombre']
                del dfA['capellidos']
                del dfB['capellidos']
                del dfA['ctelefono']
                del dfB['ctelefono']
                save_docs(df, dfA, dfB, db, 'data.persons')
    return {'name': 'person_linkage_task', 'finished': True}


@shared_task
def project_call_linkage_task():
    logging.info('project_call_linkage_task: started')
    with Mongodb() as mongodb:
        db = mongodb.db
        c = db['data.project-call']
        c.delete_many({})
        cols = [col for col in db.collection_names() if col.startswith('structured.project-call.')]
        for col in cols:
            c = db[col]
            cursor = c.find({})
            dfA = pd.DataFrame(list(cursor))
            dfA['cproyecto'] = clean(clean(dfA['proyecto'], strip_accents='unicode'), replace_by_none=' ')
            dfA['cconvocatoria'] = clean(clean(dfA['convocatoria'], strip_accents='unicode'), replace_by_none=' ')
            c = db['data.projects']
            cursor = c.find({})
            dfB = pd.DataFrame(list(cursor))
            dfB['cproyecto'] = clean(clean(dfB['tituloProyecto'], strip_accents='unicode'), replace_by_none=' ')
            indexer = rl.SortedNeighbourhoodIndex(on='cproyecto', window=9)
            pairs = indexer.index(dfA, dfB)
            compare_cl = rl.Compare(pairs, dfA, dfB)
            compare_cl.exact('cproyecto', 'cproyecto', name='proyecto')
            df1 = compare_cl.vectors[compare_cl.vectors.sum(axis=1) >= 1]
            c = db['data.calls']
            cursor = c.find({})
            dfC = pd.DataFrame(list(cursor))
            dfC['cconvocatoria'] = clean(clean(dfC['tituloConvocatoria'], strip_accents='unicode'), replace_by_none=' ')
            indexer = rl.SortedNeighbourhoodIndex(on='cconvocatoria', window=9)
            pairs = indexer.index(dfA, dfC)
            compare_cl = rl.Compare(pairs, dfA, dfC)
            compare_cl.exact('cconvocatoria', 'cconvocatoria', name='convocatoria')
            df2 = compare_cl.vectors[compare_cl.vectors.sum(axis=1) >= 1]
            docs = []
            for x, y in df1.index.tolist():
                for i, j in df2.index.tolist():
                    if x == i:
                        docs.append({
                            'proyecto': dfB.loc[y]['_id'],
                            'convocatoria': dfC.loc[j]['_id']
                        })
            c = db['data.project-call']
            bulk = c.initialize_ordered_bulk_op()
            for doc in docs:
                bulk.insert(doc)
            try:
                bulk.execute()
            except BulkWriteError as bwe:
                logging.error(bwe.details)
    return {'name': 'project_call_linkage_task', 'finished': True}


@shared_task
def project_organization_linkage_task():
    logging.info('project_organization_linkage_task: started')
    with Mongodb() as mongodb:
        db = mongodb.db
        c = db['data.project-organization']
        c.delete_many({})
        cols = [col for col in db.collection_names() if col.startswith('structured.project-organization.')]
        for col in cols:
            c = db[col]
            cursor = c.find({})
            dfA = pd.DataFrame(list(cursor))
            dfA['cproyecto'] = clean(clean(dfA['proyecto'], strip_accents='unicode'), replace_by_none=' ')
            dfA['corganizacion'] = clean(clean(dfA['organizacion'], strip_accents='unicode'), replace_by_none=' ')
            c = db['data.projects']
            cursor = c.find({})
            dfB = pd.DataFrame(list(cursor))
            dfB['cproyecto'] = clean(clean(dfB['tituloProyecto'], strip_accents='unicode'), replace_by_none=' ')
            indexer = rl.SortedNeighbourhoodIndex(on='cproyecto', window=9)
            pairs = indexer.index(dfA, dfB)
            compare_cl = rl.Compare(pairs, dfA, dfB)
            compare_cl.exact('cproyecto', 'cproyecto', name='proyecto')
            df1 = compare_cl.vectors[compare_cl.vectors.sum(axis=1) >= 1]
            c = db['data.organizations']
            cursor = c.find({})
            dfC = pd.DataFrame(list(cursor))
            dfC['corganizacion'] = clean(clean(dfC['nombre'], strip_accents='unicode'), replace_by_none=' ')
            indexer = rl.SortedNeighbourhoodIndex(on='corganizacion', window=9)
            pairs = indexer.index(dfA, dfC)
            compare_cl = rl.Compare(pairs, dfA, dfC)
            compare_cl.exact('corganizacion', 'corganizacion', name='organizacion')
            df2 = compare_cl.vectors[compare_cl.vectors.sum(axis=1) >= 1]
            docs = []
            for x, y in df1.index.tolist():
                for i, j in df2.index.tolist():
                    if x == i:
                        docs.append({
                            'proyecto': dfB.loc[y]['_id'],
                            'organizacion': dfC.loc[j]['_id']
                        })
            c = db['data.project-organization']
            bulk = c.initialize_ordered_bulk_op()
            for doc in docs:
                bulk.insert(doc)
            try:
                bulk.execute()
            except BulkWriteError as bwe:
                logging.error(bwe.details)
    return {'name': 'project_organization_linkage_task', 'finished': True}
