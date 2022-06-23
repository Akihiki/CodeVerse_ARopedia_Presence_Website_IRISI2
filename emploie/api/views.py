
""" EQUIPE : CODEVERSE
    @author : KANNOUFA FATIMA EZZAHRA
"""

from emploie.models import Planning, Presence, Seance
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import PresenceSerializer, SeanceSerializer
from django.http import FileResponse

#KANNOUFA FATIMA EZZAHRA
#   récupérer toutes les séances d'un professeur    #
@api_view(['GET'])
def getSeances(request, idProf):
    #   chercher les planning
    plannings = Planning.objects.filter(professeur_id = idProf)
    
    seances_prof = []    
    #   chercher pour chaque planning les séances qui lui correspond
    for planning in plannings:
        seances = Seance.objects.filter(planning_id = planning.id)
        seances_prof += seances

    serializer = SeanceSerializer(seances_prof, many=True)
    
    return Response(serializer.data) 

#   Modifier la présence - API  #
@api_view(['GET'])
def modifierPresenceAPI(request, idSeance, idEtudiant):
    presence = Presence.objects.get(etudiant_id = idEtudiant, seance_id = idSeance)
    presence.is_present = not presence.is_present
    presence.save()

    presences = Presence.objects.filter(seance_id = idSeance)
    serializer = PresenceSerializer(presences, many=True)
    return Response(serializer.data)
#FIROUD Reda & OUSSAHI Salma
#   retourner une image à partir de son chemin    #
def getPhoto(response, path_image):
    img = open(path_image, 'rb')
    response = FileResponse(img)

    return response
