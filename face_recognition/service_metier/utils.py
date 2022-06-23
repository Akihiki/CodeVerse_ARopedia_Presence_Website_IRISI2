
""" EQUIPE : CodeVerse et ARopedia
    @authors :  + KANNOUFA F. EZZAHRA
                + MOUZAFIR ABDELHADI
                + FIROUD REDA
                + OUSSAHI SALMA
"""

import os, cv2
from django.http.response import StreamingHttpResponse

from users.models import Students
from .classVideo import VideoCamera
from PIL import Image
import numpy as np
from semestre.models import Groupe, AnneUniversitaire
from emploie.models import Planning
import calendar
from datetime import date, datetime

from semestre.models import AnneUniversitaire, Groupe


CAMERA_PORT = 2

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
        
def getFaceDetectorXML():
    return cv2.CascadeClassifier("face_recognition/service_metier/models/face_detection.xml")

def getHaarcascadeXML():
    return cv2.CascadeClassifier("face_recognition/service_metier/models/haarcascade_frontalface_default.xml")

def getModel(filiere, niveau, groupe):
    print('face_recognition/service_metier/saved_model/'+ filiere +'/' + niveau +'/' + groupe +'/s_model_'+ filiere + '_' + niveau +'_' + groupe+ '.yml')
    return 'face_recognition/service_metier/saved_model/'+ filiere +'/' + niveau +'/' + groupe +'/s_model_'+ filiere + '_' + niveau +'_' + groupe+ '.yml'



path_dataset = "face_recognition/service_metier/dataset/"
      
def gen(camera):
    while True:
        frame = camera.get_frame()
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
        elif camera.count >= 50:
            print("Successfully Captured")
            break
        else:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def video_feed(request, id):
    print(id)
    assure_path_exists(path_dataset) 
    return StreamingHttpResponse(gen(VideoCamera(id)),
                                 content_type='multipart/x-mixed-replace; boundary=frame')
    

# récuperer les étudiants à partir de leur groupe/niveau/filiere
def getStudentsByGrp(filiere, niveau, groupe):
    # récuperer l'id du groupe
    groupe = Groupe.objects.get(nom_group=groupe, niveau__nom_niveau=niveau, niveau__filiere__nom_filiere=filiere)
    
    students = []
    year = int(datetime.today().year)
    if(datetime.today().month>=9 and datetime.today().month<=12):
        value=str(year)+"/"+str(year+1)
    else:
        value=str(year-1)+"/"+str(year)
    # on cherche les étudiants associés à cet groupe dans la table AnneeUniversitaire
    students_grp = AnneUniversitaire.objects.filter(group_id=groupe.id, libelle=value)
    for student_grp in students_grp:
        students += [student_grp.etudiant]
        
    return students


# recupérer le chemin de dossier des images pour les étudiants d'un groupe donné
def getPaths(filiere, niveau, groupe):
    paths = []
    students = getStudentsByGrp(filiere, niveau, groupe)
    
    for student in students:
        path = student.path_photos
        assure_path_exists(path)
        paths += [path]
        
    return paths
    
#FIROUD REDA & OUSSAHI SALMA
# récupérer les plannings à partir du salle 
def getDataFromPlanning(idSalle):
    # récuperer le nom du jour actuel
    day = calendar.day_name[date.today().weekday()]
    
    # plannings qui ont la salle <idSalle> et programmé dans le jour/heure acutel
    plannings = Planning.objects.filter(salle_id=idSalle, jour=day.upper())
    
    mes_plannings = []
    for planning in plannings:
        heure_deb = planning.heure_debut
        heure_fin = planning.heure_fin
        current_time = datetime.now().time() 
        
        if (heure_deb < current_time and heure_fin > current_time):
            mes_plannings += [planning]
            
    return mes_plannings


# faire la correspondance entre un visage et l'id de l'étudiant correspondant  
def getImagesAndLabels(filiere, niveau, groupe):
    detector = getFaceDetectorXML()
    faceSamples=[]
    ids = []
  
    list_dir = getPaths(filiere, niveau, groupe)

    for i in range(len(list_dir)):  
        path_imgs = list_dir[i]
        list_images = os.listdir(path_imgs)
        
        for i in range(len(list_images)):
            imagePath = path_imgs + '/' + list_images[i]
            id = int(os.path.split(imagePath)[-1].split(".")[1])
            
            print("traitement de : " + imagePath + "------>id " + str(id))
            
            PIL_img = Image.open(imagePath).convert('L')
            img_numpy = np.array(PIL_img,'uint8')
            faces = detector.detectMultiScale(img_numpy)
            
            for (x,y,w,h) in faces:
                faceSamples.append(img_numpy[y:y+h,x:x+w])
                ids.append(id)

    return faceSamples,ids


###       Backup         ###

#   enregistrement des images
def backup(filiere, niveau, groupe, idSeance):
    path_dir = "face_recognition/service_metier/backup/" + filiere + "/" + niveau + "/" + groupe + "/" + str(idSeance) + "/"
    assure_path_exists(path_dir)
    
    folder_path = "face_recognition/service_metier/folder/"
    list_images = os.listdir(folder_path)
    
    for i in range(len(list_images)):
        imagePath = folder_path + list_images[i]
        img = cv2.imread(imagePath)
        new_path = path_dir + str(i+1) + '_' + predictionImage(imagePath, filiere, niveau, groupe)
        print(imagePath)
        cv2.imwrite(new_path, img)
  
# reconnaitre l'étudiant dans une image
def predictionImage(path_img, filiere, niveau, groupe):
    img = cv2.imread(path_img)
    
    label= 'Unknown.jpg'
    
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('face_recognition/service_metier/saved_model/'+ filiere +'/' + niveau +'/' + groupe +'/s_model_'+ filiere + '_' + niveau +'_' + groupe+ '.yml')
    
    faceCascade = getFaceDetectorXML()
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5, minSize=(30, 30))
    
    for (x, y, w, h) in faces:
        Id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
        etudiant = Students.objects.get(pk=Id)
        if ((100 - confidence) > 10):
            label = 'etudiant_' + str(etudiant.id) + "_{0:.2f}".format(round(100 - confidence, 2)) + '.jpg'
        
    return label       


# récupérer l'image qui a la meileure accuracy
def photo_accuracy(path , idEtudiant):
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

#FIROUD REDA & OUSSAHI SALMA
# retourner les images d'une séance (liste présence)
def getImagesFromBackup(filiere, niveau, groupe, idSeance):
    path = filiere + "/" + niveau + "/" + groupe + "/" + str(idSeance) + "/"
    path_dir = "face_recognition/service_metier/backup/" + path
    
    assure_path_exists(path_dir)
    list_images = os.listdir(path_dir)
    
    images = []
    for i in range(len(list_images)):
        imagePath = path + list_images[i]
        images += [imagePath]
        
    return images