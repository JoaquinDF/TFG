from mongoengine import *


class Convocatoria(Document):
    tituloConvocatoria = StringField()
    fechaFinPresentacion = StringField()
    presupuesto = StringField()

    meta = {
        'collection': 'data.calls'
    }


class Proyecto(Document):
    tituloProyecto = StringField()
    estado = StringField(default='CONCEDIDO')
    fechaInicio = StringField(default=None)
    fechaFin = StringField(default=None)
    presupuestoPresentado = StringField()
    presupuestoAceptado = StringField()
    prestamo = StringField()
    subvencion = StringField()

    meta = {
        'collection': 'data.projects'
    }


class Direccion(EmbeddedDocument):
    calle = StringField()
    cp = StringField()
    ciudad = StringField()
    pais = StringField(default='')
    european = BooleanField(default=False)


class Organizacion(Document):
    nombre = StringField()
    cif = StringField()
    direccion = EmbeddedDocumentField(Direccion)
    sector = ListField(StringField())

    meta = {
        'collection': 'data.organizations'
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


class ProyectoConvocatoria(Document):
    proyecto = StringField()
    convocatoria = StringField()

    meta = {
        'collection': 'data.project-call'
    }


class ProyectoOrganizacion(Document):
    proyecto = StringField()
    organizacion = StringField()

    meta = {
        'collection': 'data.project-organization'
    }


class PersonaProyecto(Document):
    persona = StringField()
    proyecto = StringField()
    tipoRelaccion = StringField(default='CONTACTO')

    meta = {
        'collection': 'data.person-organization'
    }


class OrganizationMetric(Document):
    organization = StringField()
    numeroProyectos = StringField()
    porcentajeSubvencionado = StringField()
    subvencionTotal = StringField()
    presupuetoAceptadoTotal = StringField()

    meta = {
        'collection': 'data.organization-metric'
    }


class RegionMetric(Document):
    country = StringField()
    subvencionTotal = StringField()
    presupuetoAceptadoTotal = StringField()
    porcentajesubvencionado = StringField()
    numeroProyectos = StringField()
    numeroEmpresas = StringField()

    meta = {
        'collection': 'data.region-metric'
    }


class PersonaOrganizacion(Document):
    persona = StringField()
    organizacion = StringField()
    tipoRelaccion = StringField(default='CONTACTO')

    meta = {
        'collection': 'data.person-organization'
    }


class Community(Document):
    communityId = StringField()
    communityProjects = ListField(StringField())

    meta = {
        'collection': 'data.community'
    }
