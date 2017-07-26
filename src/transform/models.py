from mongoengine import *


class ConvocatoriaMapper(Document):
    collection = StringField(required=True)
    key = StringField(required=True)
    tituloConvocatoria = StringField(required=True)
    fechaFinPresentacion = StringField()
    presupuesto = StringField()

    meta = {
        'collection': 'mapper.calls'
    }


class ProyectoMapper(Document):
    collection = StringField(required=True)
    key = StringField(required=True)
    tituloProyecto = StringField(required=True)
    fechaInicio = StringField()
    fechaFin = StringField()
    presupuestoPresentado = StringField()
    presupuestoAceptado = StringField()
    prestamo = StringField()
    subvencion = StringField()

    meta = {
        'collection': 'mapper.projects'
    }


class Direccion(EmbeddedDocument):
    calle = StringField()
    cp = StringField()
    ciudad = StringField()


class OrganizacionMapper(Document):
    collection = StringField(required=True)
    key = StringField(required=True)
    nombre = StringField(required=True)
    cif = StringField()
    direccion = EmbeddedDocumentField(Direccion)
    sector = StringField()

    meta = {
        'collection': 'mapper.organizations'
    }


class PersonaMapper(Document):
    collection = StringField(required=True)
    key = StringField(required=True)
    nombre = StringField(required=True)
    apellidos = StringField(required=True)
    dni = StringField()
    telefono = StringField()
    email = StringField()
    validacion = StringField()

    meta = {
        'collection': 'mapper.persons'
    }


class ProyectoConvocatoriaMapper(Document):
    collection = StringField(required=True)
    proyecto = StringField(required=True)
    convocatoria = StringField(required=True)

    meta = {
        'collection': 'mapper.project-call'
    }


class ProyectoOrganizacionMapper(Document):
    collection = StringField(required=True)
    proyecto = StringField(required=True)
    organizacion = StringField(required=True)

    meta = {
        'collection': 'mapper.project-organization'
    }


class PersonaProyectoMapper(Document):
    collection = StringField(required=True)
    persona = StringField(required=True)
    proyecto = StringField(required=True)
    tipoRelaccion = StringField(default='Contacto')

    meta = {
        'collection': 'mapper.person-organization'
    }


class PersonaOrganizacionMapper(Document):
    collection = StringField(required=True)
    persona = StringField(required=True)
    organizacion = StringField(required=True)
    tipoRelaccion = StringField(default='Contacto')

    meta = {
        'collection': 'mapper.person-organization'
    }
