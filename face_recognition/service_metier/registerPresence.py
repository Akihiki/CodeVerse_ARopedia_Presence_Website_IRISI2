
""" EQUIPE : CodeVerse et ARopedia
    @authors :  + KANNOUFA F. EZZAHRA
                + MOUZAFIR ABDELHADI
"""


from requests import Response
from emploie.api.serializers import PresenceSerializer
from emploie.models import Presence, Seance
from datetime import date

from .utils import backup, getStudentsByGrp, getDataFromPlanning
from .face_recognition import facerecognition


def registerPresenceDB(idSalle):
    plannings = getDataFromPlanning(idSalle)

    for planning in plannings:
        # enregistrement d'une séance pour ce planning
        seance = Seance(planning_id=planning.id, date=date.today())
        seance.save()

        filiere = planning.groupe.niveau.filiere.nom_filiere
        niveau = planning.groupe.niveau.nom_niveau
        groupe = planning.groupe.nom_group

        # récupérer les etudiants détecter pour le groupe de ce planning
        detected_students = facerecognition(filiere, niveau, groupe)

        # récupérer TOUS les etudiants pour le groupe de ce planning

        students = getStudentsByGrp(filiere, niveau, groupe)

        students_with_presence = []

        # enregister la présence dans la base de données
        for student in students:
            if student in detected_students:
                presence = Presence(libelle='Séance : ' + str(seance.date),
                                    etudiant_id=student.id,
                                    is_present=True,
                                    seance_id=seance.id)
                presence.save()
                students_with_presence += [presence]
                print(str(student.id) + " - " +
                      student.user.username + " --->DETECTED")
            else:
                presence = Presence(libelle='Séance : ' + str(seance.date),
                                    etudiant_id=student.id,
                                    is_present=False,
                                    seance_id=seance.id)
                presence.save()
                print(str(student.id) + " - " + student.user.username)
                students_with_presence += [presence]

        # enregister les images des étudiants
        backup(filiere, niveau, groupe, seance.id)
        
        return students_with_presence
