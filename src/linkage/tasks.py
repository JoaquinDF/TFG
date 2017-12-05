from __future__ import absolute_import, unicode_literals

import logging
import pandas as pd
import recordlinkage as rl
import utils.linkage as l

from celery import shared_task
from pymongo.errors import BulkWriteError
from recordlinkage.standardise import clean

from utils.mongodb import Mongodb


@shared_task
def call_linkage_task():
    logging.debug('calls_linkage_task: started')
    l.linkage_two_data(c_structured='structured.calls.',
                       c_data='data.calls',
                       s_key='tituloConvocatoria',
                       s_columns=[
                           {
                               'column': 'tituloConvocatoria',
                               'type': 'string',
                               'regex': None
                           }
                       ])
    logging.debug('calls_linkage_task: ended')
    results = {
        'task': 'calls_linkage_task',
        'finished': True
    }
    return results


@shared_task
def organization_linkage_task():
    logging.debug('organization_linkage_task: started')
    l.linkage_two_data(c_structured='structured.organizations.',
                       c_data='data.organizations',
                       s_key='nombre',
                       s_columns=[
                           {
                               'column': 'nombre',
                               'type': 'string',
                               'regex': r'\b(sa|sl| )\b'
                           }
                       ])
    logging.debug('organization_linkage_task: ended')
    results = {
        'task': 'organization_linkage_task',
        'finished': True
    }
    return results


@shared_task
def project_linkage_task():
    logging.debug('project_linkage_task: started')
    l.linkage_two_data(c_structured='structured.projects.',
                       c_data='data.projects',
                       s_key='tituloProyecto',
                       s_columns=[
                           {
                               'column': 'tituloProyecto',
                               'type': 'string',
                               'regex': None
                           }
                       ])
    logging.debug('project_linkage_task: ended')
    results = {
        'task': 'project_linkage_task',
        'finished': True
    }
    return results


@shared_task
def person_linkage_task():
    logging.debug('person_linkage_task: started')
    l.linkage_two_data(c_structured='structured.persons.',
                       c_data='data.persons',
                       s_key='telefono',
                       s_columns=[
                           {
                               'column': 'nombre',
                               'type': 'string',
                               'regex': None
                           },
                           {
                               'column': 'apellidos',
                               'type': 'string',
                               'regex': None
                           },
                           {
                               'column': 'telefono',
                               'type': 'phonenumber',
                           }
                       ])
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
