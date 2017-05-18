from mongoengine import *


class Organization(Document):
    collection = StringField()
    identification = StringField()

    meta = {
        'collection': 'data.organizations'
    }
