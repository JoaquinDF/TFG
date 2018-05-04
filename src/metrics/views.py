import pprint

from bson.objectid import ObjectId
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from utils.mongodb import Mongodb


# PorcentajeSubvencionado

class PorcentajeSubvencionadoViewSet(ViewSet):
    def create(self, request):
        pprint.pprint(request)
        idorganization = request.data.get('id', '*')
        with Mongodb() as mongodb:
            db = mongodb.db

            cursorProjectOrganizations = db['data.project-organization']
            data = cursorProjectOrganizations.find({'organizacion': ObjectId(idorganization)})
            proyectos = [k['proyecto'] for k in data]
            porcentaje = 0
            subvencion = 0
            presupuestoAceptado = 0
            cursorProject = db['data.projects']
            for proyecto in proyectos:
                a = (cursorProject.find({'_id': ObjectId(proyecto)}))
                for presupuesto in a:
                    porcentaje += float(presupuesto['subvencion']) / float(presupuesto['presupuestoAceptado'])

                lsub = a.count()

                if (len(proyectos)):
                    porcentaje = (porcentaje / len(proyectos))
                else:
                    porcentaje = 0
        return Response(porcentaje)
