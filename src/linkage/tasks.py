from __future__ import absolute_import, unicode_literals

import logging
import pandas as pd
import recordlinkage as rl
import utils.linkage as l

from celery import shared_task
from pymongo.errors import BulkWriteError
from recordlinkage.standardise import clean, phonenumbers

from utils.mongodb import Mongodb


@shared_task
def call_linkage_task():
    logging.debug('calls_linkage_task: started')
    with Mongodb() as mongodb:
        db = mongodb.db
        cols = [col for col in db.collection_names() if col.startswith('structured.calls.')]
        for col in cols:
            c = db[col]
            cursor = c.find({})
            dfa = pd.DataFrame(list(cursor))
            dfa['ctituloConvocatoria'] = clean(clean(dfa['tituloConvocatoria'], strip_accents='unicode'), replace_by_none=' ')
            collection = db['data.calls']
            cursor = collection.find({})
            if collection.count() == 0:
                del dfa['ctituloConvocatoria']
                l.duplicate_collection(dfa, db, 'data.calls')
            else:
                dfb = pd.DataFrame(list(cursor))
                dfb['ctituloConvocatoria'] = clean(clean(dfb['tituloConvocatoria'], strip_accents='unicode'), replace_by_none=' ')
                indexer = rl.SortedNeighbourhoodIndex(on='ctituloConvocatoria', window=9)
                pairs = indexer.index(dfa, dfb)
                compare_cl = rl.Compare(pairs, dfa, dfb, low_memory=True)
                # compare_cl.string('ctituloConvocatoria','ctituloConvocatoria', 'damerau_levenshtein', threshold=.9, name='tituloConvocatoria')
                compare_cl.exact('ctituloConvocatoria', 'ctituloConvocatoria', name='tituloConvocatoria')
                df = compare_cl.vectors[compare_cl.vectors.sum(axis=1) >= 1]
                del dfa['ctituloConvocatoria']
                del dfb['ctituloConvocatoria']
                l.save_docs(df, dfa, dfb, db, 'data.calls')
    logging.debug('calls_linkage_task: ended')
    results = {
        'task': 'calls_linkage_task',
        'finished': True
    }
    return results


@shared_task
def organization_linkage_task():
    logging.debug('organization_linkage_task: started')
    with Mongodb() as mongodb:
        db = mongodb.db
        cols = [col for col in db.collection_names() if col.startswith('structured.organizations.')]
        for col in cols:
            c = db[col]
            cursor = c.find({})
            dfa = pd.DataFrame(list(cursor))
            dfa['cnombre'] = clean(clean(clean(dfa['nombre'], strip_accents='unicode', replace_by_none='.'), replace_by_none=r'\b(sa|sl| )\b'))
            c = db['data.organizations']
            cursor = c.find({})
            if c.count() == 0:
                del dfa['cnombre']
                l.duplicate_collection(dfa, db, 'data.organizations')
            else:
                dfb = pd.DataFrame(list(cursor))
                dfb['cnombre'] = clean(clean(clean(dfb['nombre'], strip_accents='unicode', replace_by_none='.'), replace_by_none=r'\b(sa|sl| )\b'))
                indexer = rl.SortedNeighbourhoodIndex(on='cnombre', window=9)
                pairs = indexer.index(dfa, dfb)
                compare_cl = rl.Compare(pairs, dfa, dfb, low_memory=True)
                # compare_cl.string('cnombre','cnombre', 'damerau_levenshtein', threshold=.9, name='nombre')
                compare_cl.exact('cnombre', 'cnombre', name='nombre')
                df = compare_cl.vectors[compare_cl.vectors.sum(axis=1) >= 1]
                del dfa['cnombre']
                del dfb['cnombre']
                l.save_docs(df, dfa, dfb, db, 'data.organizations')
    logging.debug('organization_linkage_task: ended')
    results = {
        'task': 'organization_linkage_task',
        'finished': True
    }
    return results


@shared_task
def project_linkage_task():
    logging.debug('project_linkage_task: started')
    with Mongodb() as mongodb:
        db = mongodb.db
        cols = [col for col in db.collection_names() if col.startswith('structured.projects.')]
        for col in cols:
            c = db[col]
            cursor = c.find({})
            dfa = pd.DataFrame(list(cursor))
            dfa['ctituloProyecto'] = clean(clean(dfa['tituloProyecto'], strip_accents='unicode'), replace_by_none=' ')
            c = db['data.projects']
            cursor = c.find({})
            if c.count() == 0:
                del dfa['ctituloProyecto']
                l.duplicate_collection(dfa, db, 'data.projects')
            else:
                dfb = pd.DataFrame(list(cursor))
                dfb['ctituloProyecto'] = clean(clean(dfb['tituloProyecto'], strip_accents='unicode'), replace_by_none=' ')
                indexer = rl.SortedNeighbourhoodIndex(on='ctituloProyecto', window=9)
                pairs = indexer.index(dfa, dfb)
                compare_cl = rl.Compare(pairs, dfa, dfb, low_memory=True)
                # compare_cl.string('ctituloProyecto','ctituloProyecto', 'damerau_levenshtein', threshold=.9, name='tituloProyecto')
                compare_cl.exact('ctituloProyecto', 'ctituloProyecto', name='tituloProyecto')
                df = compare_cl.vectors[compare_cl.vectors.sum(axis=1) >= 1]
                del dfa['ctituloProyecto']
                del dfb['ctituloProyecto']
                l.save_docs(df, dfa, dfb, db, 'data.projects')
    logging.debug('project_linkage_task: ended')
    results = {
        'task': 'project_linkage_task',
        'finished': True
    }
    return results


@shared_task
def person_linkage_task():
    logging.debug('person_linkage_task: started')
    with Mongodb() as mongodb:
        db = mongodb.db
        cols = [col for col in db.collection_names() if col.startswith('structured.persons.')]
        for col in cols:
            c = db[col]
            cursor = c.find({})
            dfa = pd.DataFrame(list(cursor))
            dfa['cnombre'] = clean(clean(dfa['nombre'], strip_accents='unicode'), replace_by_none=' ')
            dfa['capellidos'] = clean(clean(dfa['apellidos'], strip_accents='unicode'), replace_by_none=' ')
            dfa['ctelefono'] = phonenumbers(dfa['telefono'])
            c = db['data.persons']
            cursor = c.find({})
            if c.count() == 0:
                del dfa['cnombre']
                del dfa['capellidos']
                del dfa['ctelefono']
                l.duplicate_collection(dfa, db, 'data.persons')
            else:
                dfb = pd.DataFrame(list(cursor))
                dfb['cnombre'] = clean(clean(dfb['nombre'], strip_accents='unicode'), replace_by_none=' ')
                dfb['capellidos'] = clean(clean(dfb['apellidos'], strip_accents='unicode'), replace_by_none=' ')
                dfb['ctelefono'] = phonenumbers(dfb['telefono'])
                indexer = rl.SortedNeighbourhoodIndex(on='ctelefono', window=9)
                pairs = indexer.index(dfa, dfb)
                compare_cl = rl.Compare(pairs, dfa, dfb, low_memory=True)
                # compare_cl.string('cnombre','cnombre', 'damerau_levenshtein', threshold=.9, name='nombre')
                compare_cl.exact('cnombre', 'cnombre', name='nombre')
                # compare_cl.string('cnombre','cnombre', 'damerau_levenshtein', threshold=.9, name='nombre')
                compare_cl.exact('capellidos', 'capellidos', name='apellidos')
                # compare_cl.string('cnombre','cnombre', 'damerau_levenshtein', threshold=.9, name='nombre')
                compare_cl.exact('ctelefono', 'ctelefono', name='telefono')
                df = compare_cl.vectors[compare_cl.vectors.sum(axis=1) >= 1]
                del dfa['cnombre']
                del dfb['cnombre']
                del dfa['capellidos']
                del dfb['capellidos']
                del dfa['ctelefono']
                del dfb['ctelefono']
                l.save_docs(df, dfa, dfb, db, 'data.persons')
    logging.debug('person_linkage_task: ended')
    results = {
        'task': 'person_linkage_task',
        'finished': True
    }
    return results


@shared_task
def project_call_linkage_task():
    logging.debug('project_call_linkage_task: started')
    with Mongodb() as mongodb:
        db = mongodb.db
        c = db['data.project-call']
        c.delete_many({})
        cols = [col for col in db.collection_names() if col.startswith('structured.project-call.')]
        for col in cols:
            c = db[col]
            cursor = c.find({})
            dfa = pd.DataFrame(list(cursor))
            dfa['cproyecto'] = clean(clean(dfa['proyecto'], strip_accents='unicode'), replace_by_none=' ')
            dfa['cconvocatoria'] = clean(clean(dfa['convocatoria'], strip_accents='unicode'), replace_by_none=' ')
            c = db['data.projects']
            cursor = c.find({})
            dfb = pd.DataFrame(list(cursor))
            dfb['cproyecto'] = clean(clean(dfb['tituloProyecto'], strip_accents='unicode'), replace_by_none=' ')
            indexer = rl.SortedNeighbourhoodIndex(on='cproyecto', window=9)
            pairs = indexer.index(dfa, dfb)
            compare_cl = rl.Compare(pairs, dfa, dfb)
            compare_cl.exact('cproyecto', 'cproyecto', name='proyecto')
            df1 = compare_cl.vectors[compare_cl.vectors.sum(axis=1) >= 1]
            c = db['data.calls']
            cursor = c.find({})
            dfc = pd.DataFrame(list(cursor))
            dfc['cconvocatoria'] = clean(clean(dfc['tituloConvocatoria'], strip_accents='unicode'), replace_by_none=' ')
            indexer = rl.SortedNeighbourhoodIndex(on='cconvocatoria', window=9)
            pairs = indexer.index(dfa, dfc)
            compare_cl = rl.Compare(pairs, dfa, dfc)
            compare_cl.exact('cconvocatoria', 'cconvocatoria', name='convocatoria')
            df2 = compare_cl.vectors[compare_cl.vectors.sum(axis=1) >= 1]
            docs = []
            for x, y in df1.index.tolist():
                for i, j in df2.index.tolist():
                    if x == i:
                        docs.append({
                            'proyecto': dfb.loc[y]['_id'],
                            'convocatoria': dfc.loc[j]['_id']
                        })
            c = db['data.project-call']
            bulk = c.initialize_ordered_bulk_op()
            for doc in docs:
                bulk.insert(doc)
            try:
                bulk.execute()
            except BulkWriteError as bwe:
                logging.error(bwe.details)
    logging.debug('project_call_linkage_task: ended')
    results = {
        'task': 'project_call_linkage_task',
        'finished': True
    }
    return results


@shared_task
def project_organization_linkage_task():
    logging.debug('project_organization_linkage_task: started')
    with Mongodb() as mongodb:
        db = mongodb.db
        c = db['data.project-organization']
        c.delete_many({})
        cols = [col for col in db.collection_names() if col.startswith('structured.project-organization.')]
        for col in cols:
            c = db[col]
            cursor = c.find({})
            dfa = pd.DataFrame(list(cursor))
            dfa['cproyecto'] = clean(clean(dfa['proyecto'], strip_accents='unicode'), replace_by_none=' ')
            dfa['corganizacion'] = clean(clean(dfa['organizacion'], strip_accents='unicode'), replace_by_none=' ')
            c = db['data.projects']
            cursor = c.find({})
            dfb = pd.DataFrame(list(cursor))
            dfb['cproyecto'] = clean(clean(dfb['tituloProyecto'], strip_accents='unicode'), replace_by_none=' ')
            indexer = rl.SortedNeighbourhoodIndex(on='cproyecto', window=9)
            pairs = indexer.index(dfa, dfb)
            compare_cl = rl.Compare(pairs, dfa, dfb)
            compare_cl.exact('cproyecto', 'cproyecto', name='proyecto')
            df1 = compare_cl.vectors[compare_cl.vectors.sum(axis=1) >= 1]
            c = db['data.organizations']
            cursor = c.find({})
            dfc = pd.DataFrame(list(cursor))
            dfc['corganizacion'] = clean(clean(dfc['nombre'], strip_accents='unicode'), replace_by_none=' ')
            indexer = rl.SortedNeighbourhoodIndex(on='corganizacion', window=9)
            pairs = indexer.index(dfa, dfc)
            compare_cl = rl.Compare(pairs, dfa, dfc)
            compare_cl.exact('corganizacion', 'corganizacion', name='organizacion')
            df2 = compare_cl.vectors[compare_cl.vectors.sum(axis=1) >= 1]
            docs = []
            for x, y in df1.index.tolist():
                for i, j in df2.index.tolist():
                    if x == i:
                        docs.append({
                            'proyecto': dfb.loc[y]['_id'],
                            'organizacion': dfc.loc[j]['_id']
                        })
            c = db['data.project-organization']
            bulk = c.initialize_ordered_bulk_op()
            for doc in docs:
                bulk.insert(doc)
            try:
                bulk.execute()
            except BulkWriteError as bwe:
                logging.error(bwe.details)
    logging.debug('project_organization_linkage_task: ended')
    results = {
        'task': 'project_organization_linkage_task',
        'finished': True
    }
    return results
