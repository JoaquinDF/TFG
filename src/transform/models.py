from mongoengine import *


class Organization(Document):
    identifier = StringField()
    name = StringField()
    activity_type = StringField()
    address = StringField()
    country = StringField()
    telephone = StringField()
    www = StringField()

    meta = {
        'collection': 'unfiltered.organizations'
    }


class OrganizationMapper(Document):
    collection = StringField(required=True)
    identifier = StringField()
    name = StringField()
    activity_type = StringField()
    address = StringField()
    country = StringField()
    telephone = StringField()
    www = StringField()

    meta = {
        'collection': 'mapper.organizations'
    }
