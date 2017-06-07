from mongoengine import *


class Organization(Document):
    identifier = StringField()
    name = StringField(required=True)
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
    identifier = StringField()
    name = StringField(required=True)
    activity_type = StringField()
    address = StringField()
    country = StringField()
    telephone = StringField()
    www = StringField()

    meta = {
        'collection': 'mapper.organizations'
    }


class Project(Document):
    identifier = StringField()
    title = StringField(required=True)
    start_date = StringField()
    end_date = StringField()
    total_cost = StringField()
    financing = StringField()

    meta = {
        'collection': 'data.projects'
    }


class ProjectMapper(Document):
    collection = StringField(required=True)
    identifier = StringField()
    title = StringField(required=True)
    start_date = StringField()
    end_date = StringField()
    total_cost = StringField()
    financing = StringField()

    meta = {
        'collection': 'mapper.projects'
    }


# TODO: define all fields
class Call(Document):
    identifier = StringField()

    meta = {
        'collection': 'data.calls'
    }


# TODO: define all fields
class CallMapper(Document):
    collection = StringField(required=True)
    identifier = StringField()

    meta = {
        'collection': 'mapper.calls'
    }
