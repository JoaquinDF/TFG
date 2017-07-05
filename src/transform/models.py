from mongoengine import *


class Convocatoria(Document):
    tituloConvocatoria = StringField()
    fechaFinPresentacion = StringField()
    presupuesto = StringField()

    meta = {
        'collection': 'data.calls'
    }


class ConvocatoriaMapper(Document):
    collection = StringField(required=True)
    key = StringField(required=True)
    tituloConvocatoria = StringField(required=True)
    fechaFinPresentacion = StringField()
    presupuesto = StringField()

    meta = {
        'collection': 'mapper.calls'
    }


class Proyecto(Document):
    tituloProyecto = StringField()
    fechaInicio = StringField()
    fechaFin = StringField()
    presupuestoPresentado = StringField()
    presupuestoAceptado = StringField()
    prestamo = StringField()
    subvencion = StringField()

    meta = {
        'collection': 'data.projects'
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


class Organizacion(Document):
    nombre = StringField()
    cif = StringField()
    direccion = EmbeddedDocumentField(Direccion)
    sector = ListField(StringField())

    meta = {
        'collection': 'data.organizations'
    }


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


class Persona(Document):
    nombre = StringField()
    apellidos = StringField()
    dni = StringField()
    telefono = StringField()
    email = StringField()
    validacion = BooleanField(default=False)

    meta = {
        'collection': 'data.persons'
    }


class PersonaMapper(Document):
    collection = StringField(required=True)
    key = StringField(required=True)
    nombre = StringField(required=True)
    apellidos = StringField(required=True)
    dni = StringField()
    telefono = StringField()
    email = StringField()

    meta = {
        'collection': 'mapper.persons'
    }


class ProyectoConvocatoria(Document):
    proyecto = StringField()
    convocatoria = StringField()

    meta = {
        'collection': 'data.project-call'
    }


class ProyectoConvocatoriaMapper(Document):
    collection = StringField(required=True)
    projecto = StringField(required=True)
    convocatoria = StringField(required=True)

    meta = {
        'collection': 'mapper.project-call'
    }


class ProyectoOrganizacion(Document):
    proyecto = StringField()
    organizacion = StringField()

    meta = {
        'collection': 'data.project-organization'
    }


class ProyectoOrganizacionMapper(Document):
    collection = StringField(required=True)
    proyecto = StringField(required=True)
    organizacion = StringField(required=True)

    meta = {
        'collection': 'mapper.project-organization'
    }


class PersonaProyecto(Document):
    persona = StringField()
    proyecto = StringField()
    tipoRelaccion = StringField()

    meta = {
        'collection': 'data.person-organization'
    }


class PersonaProyectoMapper(Document):
    collection = StringField(required=True)
    persona = StringField(required=True)
    proyecto = StringField(required=True)
    tipoRelaccion = StringField()

    meta = {
        'collection': 'mapper.person-organization'
    }


class PersonaOrganizacion(Document):
    persona = StringField()
    organizacion = StringField()
    tipoRelaccion = StringField()

    meta = {
        'collection': 'data.person-organization'
    }


class PersonaOrganizacionMapper(Document):
    collection = StringField(required=True)
    persona = StringField(required=True)
    organizacion = StringField(required=True)
    tipoRelaccion = StringField()

    meta = {
        'collection': 'mapper.person-organization'
    }
