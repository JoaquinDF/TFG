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
        'collection': 'data.organizations'
    }


class Project(Document):
    identifier = StringField()
    name = StringField()
    start_date = DateTimeField()
    end_date = DateTimeField()
    total_cost = LongField()
    financing = LongField()

    meta = {
        'collection': 'data.projects'
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


class ProjectMapper(Document):
    collection = StringField(required=True)
    identifier = StringField()
    name = StringField()
    start_date = DateTimeField()
    end_date = DateTimeField()
    total_cost = LongField()
    financing = LongField()

    meta = {
        'collection': 'mapper.projects'
    }
