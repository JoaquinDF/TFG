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


class Thematic(Document):
    identifier = StringField()
    name = StringField()
    description = StringField()

    meta = {
        'collection': 'data.thematics'
    }


class ThematicMapper(Document):
    collection = StringField(required=True)
    key = StringField(required=True)
    identifier = StringField(required=True)
    name = StringField()
    description = StringField()

    meta = {
        'collection': 'mapper.thematics'
    }


class Program(Document):
    identifier = StringField()
    title = StringField()

    meta = {
        'collection': 'data.programs'
    }


class ProgramMapper(Document):
    collection = StringField(required=True)
    key = StringField(required=True)
    identifier = StringField(required=True)
    title = StringField()

    meta = {
        'collection': 'mapper.programs'
    }


class Person(Document):
    identifier = StringField()
    firstName = StringField()
    lastName = StringField()
    telephone = StringField()
    email = StringField()

    meta = {
        'collection': 'data.persons'
    }


class PersonMapper(Document):
    collection = StringField(required=True)
    key = StringField(required=True)
    identifier = StringField(required=True)
    firstName = StringField()
    lastName = StringField()
    telephone = StringField()
    email = StringField()

    meta = {
        'collection': 'mapper.persons'
    }


class Result(Document):
    identifier = StringField()
    title = StringField()
    type = StringField()
    webItem = StringField()
    webLink = StringField()

    meta = {
        'collection': 'data.results'
    }


class ResultMapper(Document):
    collection = StringField(required=True)
    key = StringField(required=True)
    identifier = StringField()
    title = StringField()
    type = StringField()
    webItem = StringField()
    webLink = StringField()

    meta = {
        'collection': 'mapper.results'
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


class CallCall(Document):
    parent = StringField()
    child = StringField()

    meta = {
        'collection': 'data.call-call'
    }


class CallCallMapper(Document):
    collection = StringField(required=True)
    parent = StringField()
    child = StringField()

    meta = {
        'collection': 'mapper.call-call'
    }


class CallThematic(Document):
    call = StringField()
    thematic = StringField()

    meta = {
        'collection': 'data.call-thematic'
    }


class CallThematicMapper(Document):
    collection = StringField(required=True)
    call = StringField()
    thematic = StringField()

    meta = {
        'collection': 'mapper.call-thematic'
    }


class PersonOrganization(Document):
    person = StringField()
    organization = StringField()

    meta = {
        'collection': 'data.person-organization'
    }


class PersonOrganizationMapper(Document):
    collection = StringField(required=True)
    person = StringField()
    organization = StringField()

    meta = {
        'collection': 'mapper.person-organization'
    }


class ProjectResult(Document):
    project = StringField()
    result = StringField()

    meta = {
        'collection': 'data.project-result'
    }


class ProjectResultMapper(Document):
    collection = StringField(required=True)
    project = StringField()
    result = StringField()

    meta = {
        'collection': 'mapper.project-result'
    }
