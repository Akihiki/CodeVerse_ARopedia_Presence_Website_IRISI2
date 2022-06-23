import os, cv2

from emploie.models import Planning, Presence, Seance
import calendar
from datetime import date, datetime

from semestre.models import AnneUniversitaire, Groupe
from users.models import Students
from service_metier.face_recognition import automatic_brightness_and_contrast
from service_metier.utils import *

def test():
    path="dataset/"
    
    list_dir = os.listdir(path)
    print(list_dir)


    for i in range(len(list_dir)):  
        path_imgs = path + list_dir[i]
        print(path_imgs) # dossier
        list_images = os.listdir(path_imgs)
        
        for i in range(len(list_images)):
            imagePath = path_imgs + '/' + list_images[i]
            print(imagePath)
            id = int(os.path.split(imagePath)[-1].split(".")[1])
            print("------>id " + str(id))

# modifier le nom des images pour chaque étudiant
def modifierUnDir(path, id):
    list_images = os.listdir(path)
        
    for i in range(len(list_images)):
        path_img = path + list_images[i]
        print(path_img)
        
        # on modifie le nom de chaque image
        new_name = path + 'Etudiant.' + str(id) + '.' + str(i+1) + '.jpg'
        os.rename(path_img, new_name) 



# modifierUnDir("../service_metier/dataset/Etudiant_Oussahi_Salma/", 804)      


# recupérer le chemin de dossier des images pour les étudiants d'un groupe donnée
def getPathDir(filiere, niveau, groupe):
    paths = []
    # récuperer l'id du groupe
    groupe = Groupe.objects.get(nom_group=groupe, niveau__nom_niveau=niveau, niveau__filiere__nom_filiere=filiere)
    groupe_id = groupe.id
    print('groupe_id' + str(groupe_id))
    # on cherche les étudiants associés à cet groupe dans la table AnneeUniversitaire
    students_grp = AnneUniversitaire.objects.filter(group_id=groupe_id)
    for student_grp in students_grp:
        path = student_grp.etudiant.path_photos
        paths += [path]
        
    return paths
    
    
    
paths = getPathDir("IRISI", "IRISI_2", "G1")

for path in paths:
    print(path)
    
    
# TEST DU MODELE

def TesterModel(request):
    camera_port = 0

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    recognizer.read('face_recognition\service_metier\saved_model\IRISI\IRISI_2\G1\s_model_IRISI_IRISI_2_G1.yml')

    faceCascade = cv2.CascadeClassifier("face_recognition/service_metier/models/face_detection.xml")

    cam = cv2.VideoCapture(camera_port )

    while True:
        ret, img =cam.read()

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(gray, 1.2,5)

        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x-20,y-20), (x+w+20,y+h+20), (0,255,0), 2)

            Id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            
            # récupérer l'etudiant à partir de son id
            etudiant = Students.objects.get(pk=Id)

            if((100 - confidence)>10):
                label = etudiant.user.first_name + ' ' + etudiant.user.last_name + " {0:.2f}%".format(round(100 - confidence, 2))
                
                cv2.rectangle(img, (x-20,y-85), (x+w+20, y-20), (0,255,0), -1)
                cv2.putText(img, label, (x,y-40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
            else :
                cv2.putText(img,"non reconnu" , (x,y-40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
                
        cv2.imshow('face recognition', img) 

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cam.release()

    cv2.destroyAllWindows()
    

def TesterModelUpgraded(request):
    label = "Unknown"
    camera_port = 0

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    recognizer.read('face_recognition/service_metier/saved_model/IRISI/IRISI_2/G1/s_model_IRISI_IRISI_2_G1.yml')

    faceCascade = getFaceDetectorXML()

    cam = cv2.VideoCapture(camera_port )

    while True:
        ret, img =cam.read()
        
        auto_result, alpha, beta = automatic_brightness_and_contrast(img)
       
        gray = cv2.cvtColor(auto_result, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in faces:
            
            cv2.rectangle(img, (x-20,y-20), (x+w+20,y+h+20), (0,255,0), 2)
            Id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            
            # récupérer l'etudiant à partir de son id
            etudiant = Students.objects.get(pk=Id)

            if((100 - confidence)>10):
                label = etudiant.user.first_name + ' ' + etudiant.user.last_name + " {0:.2f}%".format(round(100 - confidence, 2))
                
                cv2.rectangle(img, (x-20,y-85), (x+w+20, y-20), (0,255,0), -1)
                cv2.putText(img, label, (x,y-40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
            else :
                cv2.putText(img,"non reconnu" , (x,y-40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

        cv2.imshow('face recognition', img) 
        
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cam.release()

    cv2.destroyAllWindows()
    
    
def getPlanningByDate(filiere='IRISI', niveau='IRISI_2', groupe='G1'):
    groupe = Groupe.objects.get(nom_group=groupe, niveau__nom_niveau=niveau, niveau__filiere__nom_filiere=filiere)
    groupe_id = groupe.id
    print('groupe_id' + str(groupe_id))
    
    # récuperer le nom du jour actuel
    day = calendar.day_name[date.today().weekday()]
    # plannings de ce groupe
    plannings = Planning.objects.filter(groupe_id=groupe_id, jour=day.upper())
    print(plannings)
    for planning in plannings : 
        heure_deb = planning.heure_debut
        heure_fin = planning.heure_fin
        current_time = datetime.now().time()
        print(str(current_time) + " IS BETWEEN " + str(heure_deb) + " et " + str(heure_fin))
        if (heure_deb < current_time and heure_fin > current_time):
            print("--> res = " + planning.libelle + " TRUE")
        else:
            print("--> res = " + planning.libelle + " FALSE")

     
getPlanningByDate()   

def myFCT(filiere, niveau, groupe):
     # enregistrement de la séance
    # id_planning
    seance = Seance(id=261, planning_id=28, date=date.today())
    seance.save()
    
    detected_students = facerecognition(filiere, niveau, groupe)
    print("\n\nDETECTED STUDENTS\n")
    for student in detected_students:
        print(str(student.id) + " - " + student.user.username)

    print("\n\nSTUDENTS\n")
    students =  getStudentsByGrp(filiere, niveau, groupe)
    for student in students:
        if student in detected_students:
            presence = Presence(libelle='Séance : ' + str(seance.date),
                            etudiant_id= student.id,
                            is_present=True,
                            seance_id= seance.id)
            presence.save()
            print(str(student.id) + " - " + student.user.username + " --->DETECTED")
        
        else:
            presence = Presence(libelle='Séance : ' + str(seance.date),
                            etudiant_id= student.id,
                            is_present=False,
                            seance_id= seance.id)
            presence.save()
            print(str(student.id) + " - " + student.user.username)
            

        
        
now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time ="+ current_time)


#######################
# SELECT * FROM `emploie_planning` WHERE salle_id=2 AND jour='THURSDAY'
# récuprer le Filiere/Niveau/grp à partir du idSeance dans la table Planning

def getDataFromPlanning(idSalle):
    # récuperer le nom du jour actuel
    day = calendar.day_name[date.today().weekday()]
    
    # planning qui ont la salle <idSalle> et programmé dans le jour/heure acutel
    plannings = Planning.objects.filter(salle_id=idSalle, jour=day.upper())
    
    mes_plannings = []
    for planning in plannings:
        heure_deb = planning.heure_debut
        heure_fin = planning.heure_fin
        current_time = datetime.now().time() 
        
        if (heure_deb < current_time and heure_fin > current_time):
            mes_plannings += [planning]
            
    return mes_plannings
        

plannings = getDataFromPlanning(2)
##################
# filiere/niveau/groupe de chaque planning
##print(planning)
#print('groupe ' + planning.groupe.nom_group)
#print('niveau ' + planning.groupe.niveau.nom_niveau)
#print('filiere ' + planning.groupe.niveau.filiere.nom_filiere)
#print(str(current_time) + " IS BETWEEN " + str(heure_deb) + " et " + str(heure_fin))
#print("--> res = " + planning.libelle + " TRUE")

########### FACE RECOGNITION

def facerecognition(filiere, niveau, groupe):
    detected_persons=set()
    label = "Unknown"
    
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    path_model = 'face_recognition/service_metier/saved_model/'+ filiere +'/' + niveau +'/' + groupe +'/s_model_'+ filiere + '_' + niveau +'_' + groupe+ '.yml'
    recognizer.read(path_model)
    faceCascade = getFaceDetectorXML()
    imagePaths = [os.path.join("face_recognition/service_metier/folder", f) for f in os.listdir("face_recognition/service_metier/folder")]
    print(imagePaths)
    i = 0
    for imagePath in imagePaths:
        i = i + 1
        print(imagePath)
        img = cv2.imread(imagePath).copy()
        auto_result, alpha, beta = automatic_brightness_and_contrast(img)
        
        gray = cv2.cvtColor(auto_result, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in faces:
            Id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            
            # récupérer l'etudiant à partir de son id
            etudiant = Students.objects.get(id=Id)
            
            if ((100 - confidence) > 10):
                label = etudiant.user.username
                detected_persons.add(etudiant)
                print("id = " + str(label))
            else:
                print(label)
    
    return detected_persons

#######################
def facerecognitionMOUZAFIR():
    detected_persons=set()
    label = "Unknown"
    camera_port = 0

    etudiants = {
    
    6 : "mOUZAFIR",
    3 : "fATIMA",
    9 : "Aminatou",
    8 : "Sami",
    4 : "fIROUD",
}

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    recognizer.read('face_recognition/service_metier/saved_model/IRISI/IRISI_1/G1/s_model_IRISI_IRISI_1_G1.yml')

    faceCascade = getFaceDetectorXML()

    # cam = cv2.VideoCapture(camera_port )

    # while True:
    imagePaths = [os.path.join("face_recognition/service_metier/folder", f) for f in os.listdir("face_recognition/service_metier/folder")]
    print(imagePaths)
    i = 0
    for imagePath in imagePaths:
        i = i + 1
        print(imagePath)
        # ret, img =cam.read()
        img = cv2.imread(imagePath).copy()
        
        
        auto_result, alpha, beta = automatic_brightness_and_contrast(img)
        # cv2.imshow('face recognition'+str(i), auto_result)
       
        gray = cv2.cvtColor(auto_result, cv2.COLOR_BGR2GRAY)
        print(gray)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5, minSize=(30, 30))
        print(faces)
        for (x, y, w, h) in faces:
            # cv2.rectangle(img, (x - 20, y - 20), (x + w + 20, y + h + 20), (0, 255, 0), 2)

            Id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

            if ((100 - confidence) > 10):
                label = etudiants[Id] + " {0:.2f}%".format(round(100 - confidence, 2))
                detected_persons.add(etudiants[Id])
                print(label)
            else:
                # cv2.putText(img, "non reconnu", (x, y - 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                print(label)

        # cv2.imshow('face recognition', img)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

        # while (True):
        #     # cv2.imshow('frame', auto_result);
        #     if cv2.waitKey(100) & 0xFF == ord('q'):
        #         break;

    # cam.release()

    return detected_persons

############# LIAISON BD
def EnregistrerEtudiantsBD(idSeance):
    plannings = getDataFromPlanning(idSeance)
    
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
        students =  getStudentsByGrp(filiere, niveau, groupe)
        
        # enregister la présence dans la base de données
        for student in students:
            if student in detected_students:
                presence = Presence(libelle='Séance : ' + str(seance.date),
                                etudiant_id= student.id,
                                is_present=True,
                                seance_id= seance.id)
                presence.save()
                print(str(student.id) + " - " + student.user.username + " --->DETECTED")
            
            else:
                presence = Presence(libelle='Séance : ' + str(seance.date),
                                etudiant_id= student.id,
                                is_present=False,
                                seance_id= seance.id)
                presence.save()
                print(str(student.id) + " - " + student.user.username)


############################ Backup

def getFaceDetectorXML():
    return cv2.CascadeClassifier("face_recognition/service_metier/models/face_detection.xml")


# renomer les images avec l'id de l'étudiant detecté
def mafct(filiere='SIR', niveau='SIR', groupe='G2', idSeance=1):
    path="face_recognition/service_metier/backup/" + filiere + '/' + niveau + '/' + groupe + '/' + str(idSeance) + '/'
    list_images = os.listdir(path)
    for i in range(len(list_images)):
        imagePath = path + list_images[i]
        label = path + str(i+1) + '_' +predictionImage(imagePath)
        print(imagePath + '---->' + label)
        # renomer l'image
        os.rename(imagePath, label) 
        
 

  
 
def predictionImage(path_img):
    img = cv2.imread(path_img)
    
    label= 'Unknown.jpg'
    
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('face_recognition/service_metier/saved_model/IRISI/IRISI_2/G1-IRISI2/s_model_IRISI_IRISI 2_G1-IRISI2.yml')
    
    faceCascade = getFaceDetectorXML()
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5, minSize=(30, 30))
    
    for (x, y, w, h) in faces:
        Id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
        etudiant = Students.objects.get(pk=Id)
        if ((100 - confidence) > 10):
            label = 'etudiant_' + str(etudiant.id) + "_{0:.2f}".format(round(100 - confidence, 2)) + '.jpg'
        
    return label

#test 
# imagePath = path + list_images[i]

predictionImage('face_recognition/service_metier/backup/SIR/SIR/G2/1/frame0.jpg')   

def photo_accuracy(filiere, niveau, groupe, idSeance , idEtudiant):
    path = path="face_recognition/service_metier/backup/" + filiere + '/' + niveau + '/' + groupe + '/' + str(idSeance) + '/'
    max = 0
    image = ''
    list_images = os.listdir(path)
    for i in range(len(list_images)):
        # on élimine les images ou personne n'est detecté
        if os.path.split(list_images[i])[-1].split("_")[1] != 'Unknown.jpg':
            # on récupère l'id de l'etudiant à partir du nom du chemin
            id = int(os.path.split(list_images[i])[-1].split("_")[2])
            if id == idEtudiant :
                accuracy = float(os.path.splitext(os.path.split(list_images[i])[-1].split("_")[3])[0])
                # on récupère l'image qui a la meileure accuracy
                if accuracy > max : 
                    max = accuracy
                    image =list_images[i]
    return image

# test 

photo_accuracy('SIR', 'SIR', 'G2', 1, 808)   