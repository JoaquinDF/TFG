from mongoengine import *


class Convocatoria(Document):
    tituloConvocatoria = StringField()
    fechaFinPresentacion = StringField()
    presupuesto = FloatField()

    meta = {
        'collection': 'data.calls'
    }


class Proyecto(Document):
    tituloProyecto = StringField()
    estado = StringField(default='CONCEDIDO')
    fechaInicio = StringField(default=None)
    fechaFin = StringField(default=None)
    presupuestoPresentado = FloatField()
    presupuestoAceptado = FloatField()
    prestamo = FloatField()
    subvencion = FloatField()

    meta = {
        'collection': 'data.projects'
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


class PersonaOrganizacion(Document):
    persona = StringField()
    organizacion = StringField()
    tipoRelaccion = StringField(default='CONTACTO')

    meta = {
        'collection': 'data.person-organization'
    }
