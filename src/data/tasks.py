from __future__ import absolute_import, unicode_literals

import json

from celery import shared_task
from utils.mongodb import Mongodb
from bson import ObjectId
import numpy as np
import pprint
import math
import sys


class UtilsCity:
    def getCity(city):

        with open('/home/bisite/innhome/innhome/src/www/static/json/jsonCity.json') as data_file:
            data = json.load(data_file)

        for (dict) in data:
            pais = ''
            # print(dict['City'].lower())
            # print(city.lower())

            if dict['City'].lower() == city.lower():
                    pais = (dict['Country'])
                    return pais
        return 'PAIS'

    def getEU(city):

        with open('/home/bisite/innhome/innhome/src/www/static/json/jsonCity.json') as data_file:
            data = json.load(data_file)

        for (dict) in data:

            if dict['City'].lower() == city.lower():
                    if 'Europe' in dict['State']:
                        print(dict['State'])
                        print(dict['City'].lower())
                        return True
        return False


@shared_task
def CreateAllMetrics():
    with Mongodb() as mongodb:
        db = mongodb.db
        cursorOrganiaztion = db['data.organizations']
        cursorProyectos = db['data.projects']
        cursorRegionMetric = db['data.region-metric']
        cursorOrganiaztionProject = db['data.project-organization']

        diff = cursorOrganiaztion.distinct('direccion.pais')

        # differentCountries = [country for country in diff if country == 'Spain']
        differentCountries = ['Europe']

        for country in differentCountries:
            Country = country
            print(country)
            databyCountry = cursorOrganiaztion.find({'direccion.european': True})
            presupuesto = 0
            presupuestofinal = 0
            presupuestoOrg = 0
            subvencion = 0
            subvencionfinal = 0
            numeroproyectos = 0
            subvencionOrg = 0
            i = 0
            for organizationbycountry in databyCountry:
                i += 1
                print(str(i) + '/' + str(databyCountry.count()))
                presupuestoOrg = 0
                subvencionOrg = 0

                ProyOrg = cursorOrganiaztionProject.find({'organizacion': organizationbycountry['_id']})

                numeroproyectos += ProyOrg.count()
                for proyectosOrg in ProyOrg:
                    proyecto = cursorProyectos.find_one({'_id': proyectosOrg['proyecto']})

                    presupuesto = 0
                    subvencion = 0
                    try:
                        x = proyecto['subvencion']
                        y = proyecto['presupuestoAceptado']

                        if math.isnan(proyecto['subvencion']):
                            proyecto['subvencion'] = '0'

                        if math.isnan(proyecto['presupuestoAceptado']):
                            proyecto['presupuestoAceptado'] = '0'


                    except Exception:
                        continue

                    presupuesto += float(proyecto['presupuestoAceptado'])
                    subvencion += float(proyecto['subvencion'])
                    presupuestoOrg += presupuesto
                    subvencionOrg += subvencion

                presupuestoOrg = presupuestoOrg / ProyOrg.count()
                subvencionOrg = subvencionOrg / ProyOrg.count()

                presupuestofinal += presupuestoOrg
                subvencionfinal += subvencionOrg
            print('-------------------------------')
            presupuestofinal = presupuestofinal / databyCountry.count()
            subvencionfinal = subvencionfinal / databyCountry.count()
            print(Country)
            print(subvencionfinal)
            print(presupuestofinal)
            print(numeroproyectos)
            porcentaje = subvencionfinal / presupuestofinal * 100

            cursorRegionMetric.insert({'country': Country,
                                       'subvencionTotal': subvencionfinal,
                                       'presupuetoAceptadoTotal': presupuestofinal,
                                       'porcentajesubvencionado': porcentaje,
                                       'numeroProyectos': numeroproyectos,
                                       'numeroEmpresas': databyCountry.count()})

    return {'addCountrytoOrganizations': 'OK'}


@shared_task
def CreateOrganizationMetrics():
    with Mongodb() as mongodb:
        db = mongodb.db
        cursorOrganiaztion = db['data.organizations']
        cursorOrganiaztionMetric = db['data.organization-metric']
        cursorProyectos = db['data.projects']
        cursorRegionMetric = db['data.region-metric']
        cursorOrganiaztionProject = db['data.project-organization']

        organizations = cursorOrganiaztion.find({}, no_cursor_timeout=True)
        presupuesto = 0
        presupuestofinal = 0
        presupuestoOrg = 0
        subvencion = 0
        subvencionfinal = 0
        numeroproyectos = 0
        subvencionOrg = 0
        i = 0
        for organization in organizations:
            idOrganization = organization['_id']
            print(str(i) + '/' + str(organizations.count()))
            i += 1
            presupuestoOrg = 0
            subvencionOrg = 0

            ProyOrg = cursorOrganiaztionProject.find({'organizacion': organization['_id']})

            print(organization['_id'])
            numeroproyectos += ProyOrg.count()
            print('--------------------')
            print('ORG NAME' + organization['nombre'])
            print(ProyOrg.count())

            for proyectosOrg in ProyOrg:
                proyecto = cursorProyectos.find_one({'_id': proyectosOrg['proyecto']})
                print('Proy NAME' + proyecto['tituloProyecto'])

                presupuesto = 0
                subvencion = 0
                try:
                    x = proyecto['subvencion']
                    y = proyecto['presupuestoAceptado']

                    if math.isnan(proyecto['subvencion']):
                        proyecto['subvencion'] = '0'

                    if math.isnan(proyecto['presupuestoAceptado']):
                        proyecto['presupuestoAceptado'] = '0'


                except Exception:
                    continue

                presupuesto += float(proyecto['presupuestoAceptado'])
                subvencion += float(proyecto['subvencion'])
                presupuestoOrg += presupuesto
                subvencionOrg += subvencion

            presupuestoOrg = presupuestoOrg / ProyOrg.count()
            subvencionOrg = subvencionOrg / ProyOrg.count()

            print('presupuesto ORG ' + str(presupuestoOrg))
            print('subvencion ORG ' + str(subvencionOrg))

            if subvencionOrg == 0:
                porcentaje = 0
            else:
                if presupuestoOrg == 0:
                    porcentaje = 0
                else:
                    porcentaje = subvencionOrg / presupuestoOrg * 100

            cursorOrganiaztionMetric.insert({'organization': idOrganization,

                                             'numeroProyectos': ProyOrg.count(),
                                             'subvencionTotal': subvencionOrg,
                                             'porcentajeSubvencionado': porcentaje,
                                             'presupuetoAceptadoTotal': presupuestoOrg,
                                             })
        organizations.close()


@shared_task
def CheckEUOrganizations():
    with Mongodb() as mongodb:
        db = mongodb.db
        c = db['data.organizations']

        data = c.find({}, no_cursor_timeout=True)
        i = 0
        for organization in data:
            i += 1

            if i % 1000 == 0:
                print(i)
            try:
                x = organization['direccion']['ciudad']

            except Exception:
                continue

            organization['direccion']['european'] = UtilsCity.getEU(organization['direccion']['ciudad'])
            db.data.organizations.save(organization)
        data.close()
    return {'addCountrytoOrganizations': 'OK'}


@shared_task
def dropduplicates():
    with Mongodb() as mongodb:
        db = mongodb.db
        cursorOrganiaztionProject = db['data.project-organization']

        data = cursorOrganiaztionProject.aggregate([
            {
                "$group": {
                    "_id": {"proyecto": "$proyecto", "organizacion": "$organizacion"},
                    "uniqueIds": {"$addToSet": "$_id"},
                    "count": {"$sum": 1}
                }
            },
            {"$match": {"count": {"$gt": 1}}}
        ])
        for duplicates in data:
            x = duplicates['uniqueIds']
            pprint.pprint(x)
            dropdata = x[1:]
            for data in dropdata:
                cursorOrganiaztionProject.remove({"_id": data});


@shared_task
def addCountrytoOrganizations():
    with Mongodb() as mongodb:
        db = mongodb.db
        c = db['data.organizations']

        data = c.find({}, no_cursor_timeout=True)
        i = 0

        for organization in data:

            i += 1

            if i % 1000 == 0:
                print(i)

            try:
                x = organization['direccion']['ciudad']

            except Exception:
                continue

            organization['direccion']['pais'] = UtilsCity.getCity(organization['direccion']['ciudad'])
            db.data.organizations.save(organization)
        data.close()

    return {'addCountrytoOrganizations': 'OK'}


@shared_task
def ReloadDataBase():
    print('Iniciando Añadir el country a las Organizacion')
    addCountrytoOrganizations()
    print('Fin de AddCountryOrganization')
    print('Añadiendo EU a las Organizaciones')
    CheckEUOrganizations()
    print('Fin Añadir EU')

    # print('Iniciando la actualización de los números')
    # UpadateAllNumbersData()
    # print('Fin de la carga')


def UpdateNumberSingleData(s):
    if len(s) == 0:
        return float('0')

    s = s.replace(' ', '')
    s = s.replace('€', '')
    s = s.replace(',', '.')
    l = s.split('.')
    n = ''
    try:
        if len(l) > 1:
            for i, j in enumerate(l):
                if i + 1 == len(l):
                    n = n + '.' + j
                else:
                    n = n + j
        else:
            n = l[0]

        return float(n)

    except Exception as e:
        s = str(e)
        print(s)
        print(n)
        sys.exit(1)


@shared_task
def UpadateAllNumbersData():
    with Mongodb() as mongodb:
        db = mongodb.db
        c = db['data.projects']
        i = 0

        data = c.find({}, no_cursor_timeout=True)

        for presupuesto in data:
            i += 1

            if i % 1000 == 0:
                print(i)

            try:
                x = presupuesto['subvencion']
                x = presupuesto['presupuestoAceptado']

            except Exception:
                continue

            presupuesto['subvencion'] = UpdateNumberSingleData(str(presupuesto['subvencion']))
            presupuesto['presupuestoAceptado'] = UpdateNumberSingleData(str(presupuesto['presupuestoAceptado']))

            db.data.projects.save(presupuesto)

        data.close()
        print(str(i) + ' Proyectos actualizadas')
    return {'UpadateAllNumbersData': 'OK'}
