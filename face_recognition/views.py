""" EQUIPE : CodeVerse et ARopedia
    @authors :  + KANNOUFA F. EZZAHRA
                + MOUZAFIR ABDELHADI
                + FIROUD REDA
                + OUSSAHI SALMA
"""

from django.shortcuts import render, redirect
import numpy as np
import cv2
from rest_framework.decorators import api_view
from rest_framework.response import Response

from emploie.api.serializers import PresenceSerializer
from .service_metier.ReglageCounter import RecognizerMethod
from .service_metier.registerPresence import registerPresenceDB
from .service_metier.utils import *
from users.models import Students


#   dashboard de l'admin pour l'entrainement du modèle
def EntrainementAdminDash(request):
    context = {}
    return render(request, 'face_recognition/pages/entrainement_modele.admin.html', context)


#   Entrainer et sauvegarder le modèle de reconnaissance
def training(request, filiere, niveau, groupe):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces, ids = getImagesAndLabels(filiere, niveau, groupe)

    print("Training ...\nWAIT !")
    recognizer.train(faces, np.array(ids))

    #   dans le dossier saved_model on enregistre le modèle dans le dossier <saved_model/nom_filiere/nom_niveau/nom_grp/>
    path_dir = 'face_recognition/service_metier/saved_model/' + \
               filiere + '/' + niveau + '/' + groupe + '/'
    assure_path_exists(path_dir)

    nom_modele = path_dir + 's_model_' + filiere + \
                 '_' + niveau + '_' + groupe + '.yml'
    recognizer.write(nom_modele)

    return redirect('EntrainementAdminDash')


# tester le modèle de reconnaissance
def TesterModel(request, filiere='IRISI', niveau='IRISI_2', groupe='G1'):
    label = "Unknown"

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    recognizer.read(
        'face_recognition/service_metier/saved_model/IRISI/IRISI 2/G1-IRISI2/s_model_IRISI_IRISI 2_G1-IRISI2.yml')

    faceCascade = getFaceDetectorXML()

    cam = cv2.VideoCapture(CAMERA_PORT)

    while True:
        ret, img = cam.read()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray, scaleFactor=1.5, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in faces:

            cv2.rectangle(img, (x - 20, y - 20), (x + w + 20, y + h + 20), (0, 255, 0), 2)
            Id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

            # récupérer l'etudiant à partir de son id
            etudiant = Students.objects.get(pk=Id)

            if ((100 - confidence) > 10):
                label = etudiant.user.first_name + ' ' + etudiant.user.last_name + \
                        " {0:.2f}%".format(round(100 - confidence, 2))

                cv2.rectangle(img, (x - 20, y - 85),
                              (x + w + 20, y - 20), (0, 255, 0), -1)
                cv2.putText(img, label, (x, y - 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            else:
                cv2.putText(img, "non reconnu", (x, y - 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('face recognition', img)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

    return redirect('EntrainementAdminDash')


def testRegisterBD(request):
    registerPresenceDB(1)
    return redirect('EntrainementAdminDash')

#FIROUD REDA & OUSSAHI SALMA
#cette fonction lance l'enregistrement de la camera depuis le telephone puis retourne les resultats avec les liens des images prise et des photo de profile pour faire le backup
@api_view(['POST'])
def RegisterFromPhone(request):
    if request.data:
        label = RecognizerMethod(request.data['body'])
        # label= registerPresenceDB(request.data['body'])
        serializer = PresenceSerializer(label, many=True)
        print(serializer.data)
        return Response(serializer.data)


#test presence
@api_view(['GET'])
def testPresenceBD(request):
        presences = registerPresenceDB(5)
        serializer = PresenceSerializer(presences, many=True)
        return Response(serializer.data)
