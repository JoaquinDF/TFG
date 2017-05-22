from mongoengine import *


class Organization(Document):
    key = StringField()
    name = StringField()
    activity_type = StringField()
    address = StringField()
    country = StringField()
    telephone = StringField()
    www = StringField()

    meta = {
        'collection': 'data.organizations'
    }


class OrganizationMapper(Document):
    collection = StringField(required=True)
    key = StringField()
    name = StringField()
    activity_type = StringField()
    address = StringField()
    country = StringField()
    telephone = StringField()
    www = StringField()

    meta = {
        'collection': 'mapper.organizations'
    }
