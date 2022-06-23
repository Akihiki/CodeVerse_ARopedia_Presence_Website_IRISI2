
""" EQUIPE : CodeVerse et ARopedia
    @authors :  + KANNOUFA F. EZZAHRA
                + FIROUD REDA
                + OUSSAHI SALMA
                + MOUZAFIR ABDELHADI
"""

from rest_framework.response import Response
from django.http import FileResponse, JsonResponse
from rest_framework.decorators import api_view
from emploie.api.serializers import PresenceSerializer

from emploie.models import Presence
from face_recognition.service_metier.utils import photo_accuracy
from ..service_metier.ReglageCounter import RecognizerMethod
from .serializers import *
from semestre.models import Groupe, Niveau
from filiere.models import  Filiere


#   Récupérer les données de Filières, Niveaux et groupes
def get_json_filiere_data(request):
    data = list(Filiere.objects.values())
    return JsonResponse({'data': data})

def get_json_niveau_data(request, filiere):
    data = list(Niveau.objects.filter(filiere__nom_filiere=filiere).values())
    return JsonResponse({'data': data})

def get_json_group_data(request, niveau):
    data = list(Groupe.objects.filter(niveau__nom_niveau=niveau).values())
    return JsonResponse({'data': data})


#   API   # #FIROUD Reda & OUSSAHI Salma
@api_view(['GET'])
def getSalles(request):
    try:
        salles = Salle.objects.all()
        serializer = SalleSerializer(salles, many=True)
        return Response(serializer.data)
    except Niveau.DoesNotExist:
        return Response([])
    
#FIROUD Reda & OUSSAHI Salma
#   retourner une image from backup     #
def getPhotoFromBackup(response, filiere, niveau, groupe, idSeance ,idEtudiant):
    path="face_recognition/service_metier/backup/" + filiere + '/' + niveau + '/' + groupe + '/' + str(idSeance) + '/'
    name_image = photo_accuracy(path, idEtudiant) 
    if name_image == '':
        path_image = 'media/avatar-default.png'
    else:
        path_image = path + name_image
    img = open(path_image, 'rb')
    print(img)
    response = FileResponse(img)

    return response


# retourne presence - test 
@api_view(['GET'])
def presenceTest(request):
    presence = Presence.objects.get(id=1)
    serializer = PresenceSerializer(presence, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def filiere_liste(request):
    try:
        filieres = Filiere.objects.all()
        serializer = FiliereSerializer(filieres, many=True)
        return Response(serializer.data)
    except Filiere.DoesNotExist:
        return Response([])


@api_view(['GET'])
def Niveau_liste(request, nom_filiere):
    try:
        filiere = Filiere.objects.get(nom_filiere__exact=nom_filiere)
        niveaus = Niveau.objects.filter(filiere_id__exact=filiere.id).all()
        serializer = NiveauSerializer(niveaus, many=True)
        return Response(serializer.data)
    except Niveau.DoesNotExist:
        return Response([])


@api_view(['POST'])
def post_niveau(request):
    if request.data:
        label = RecognizerMethod()
        return Response(
            {
                "detected faces": label,
                "success" : "success"
            },
            status=200
        )

    return Response(
        {
            "error": True,
            "error_msg": "not valid",
        },
        status=400
    )
    
