from mongoengine import *


class Organization(Document):
    collection = StringField(required=True)
    key = StringField()
    name = StringField()

    meta = {
        'collection': 'mapper.organizations'
    }
