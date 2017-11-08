from __future__ import absolute_import, unicode_literals

import json

from celery import shared_task
from utils.mongodb import Mongodb


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
def CheckEUOrganizations():
    with Mongodb() as mongodb:
        db = mongodb.db
        c = db['data.organizations']

        data = c.find({}, no_cursor_timeout=True)
        i = 0
        for organization in data:
            print(i)
            i += 1
            try:
                x = organization['direccion']['ciudad']

            except Exception:
                continue

            organization['direccion']['european'] = UtilsCity.getEU(organization['direccion']['ciudad'])
            db.data.organizations.save(organization)
        data.close()
    return {'addCountrytoOrganizations': 'OK'}



@shared_task
def addCountrytoOrganizations():
    with Mongodb() as mongodb:
        db = mongodb.db
        c = db['data.organizations']

        data = c.find({}, no_cursor_timeout=True)
        i = 0
        for organization in data:
            print(i)
            i += 1
            try:
                x = organization['direccion']['ciudad']

            except Exception:
                continue

            organization['direccion']['pais'] = UtilsCity.getCity(organization['direccion']['ciudad'])
            db.data.organizations.save(organization)
        data.close()
    return {'addCountrytoOrganizations': 'OK'}
