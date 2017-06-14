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


class OrganizationMapper(Document):
    collection = StringField(required=True)
    key = StringField(required=True)
    identifier = StringField(required=True)
    name = StringField()
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
    title = StringField()
    start_date = StringField()
    end_date = StringField()
    total_cost = StringField()
    financing = StringField()

    meta = {
        'collection': 'data.projects'
    }


class ProjectMapper(Document):
    collection = StringField(required=True)
    key = StringField(required=True)
    identifier = StringField(required=True)
    title = StringField()
    start_date = StringField()
    end_date = StringField()
    total_cost = StringField()
    financing = StringField()

    meta = {
        'collection': 'mapper.projects'
    }


class Call(Document):
    identifier = StringField()
    title = StringField()
    status = StringField()
    publication_date = StringField()

    meta = {
        'collection': 'data.calls'
    }


class CallMapper(Document):
    collection = StringField(required=True)
    key = StringField(required=True)
    identifier = StringField(required=True)
    title = StringField()
    status = StringField()
    publication_date = StringField()

    meta = {
        'collection': 'mapper.calls'
    }


class ProjectOrganization(Document):
    project = StringField()
    organization = StringField()

    meta = {
        'collection': 'data.project-organization'
    }


class ProjectOrganizationMapper(Document):
    collection = StringField(required=True)
    project = StringField()
    organization = StringField()

    meta = {
        'collection': 'mapper.project-organization'
    }


class ProjectCall(Document):
    project = StringField()
    call = StringField()

    meta = {
        'collection': 'data.project-call'
    }


class ProjectCallMapper(Document):
    collection = StringField(required=True)
    project = StringField()
    call = StringField()

    meta = {
        'collection': 'mapper.project-call'
    }
