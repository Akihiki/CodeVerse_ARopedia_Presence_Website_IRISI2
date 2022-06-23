
""" EQUIPE : CodeVerse et ARopedia
    @authors :  + KANNOUFA F. EZZAHRA
                + FIROUD REDA
                + MOUZAFIR ABDELHADI
"""

import cv2, os

from users.models import Students
from .utils import getFaceDetectorXML, getModel


# @Author by FIROUD Reda
#cette fonction diminue la luminosite d'une image dans le cadre de reconaissance
def automatic_brightness_and_contrast(image, clip_hist_percent=1):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    hist_size = len(hist)
    
    accumulator = []
    accumulator.append(float(hist[0]))
    for index in range(1, hist_size):
        accumulator.append(accumulator[index - 1] + float(hist[index]))
    
    maximum = accumulator[-1]
    clip_hist_percent *= (maximum / 100.0)
    clip_hist_percent /= 2.0
    
    minimum_gray = 0
    while accumulator[minimum_gray] < clip_hist_percent:
        minimum_gray += 1
    
    maximum_gray = hist_size - 1
    while accumulator[maximum_gray] >= (maximum - clip_hist_percent):
        maximum_gray -= 1
    
    alpha = 255 / (maximum_gray - minimum_gray)
    beta = -minimum_gray * alpha
    
    auto_result = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return (auto_result, alpha, beta)



# @authors abdelhadi mouzafir & fatima Ezzahra Kannoufa
# @recustomized by abdelhadi to fit the requirements
# Firoud reda applied data augementation
def facerecognition(filiere, niveau, groupe):
    detected_persons=set()

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    path_model = getModel(filiere, niveau, groupe)
    recognizer.read(path_model)

    faceCascade = getFaceDetectorXML()

    imagePaths = [os.path.join("face_recognition/service_metier/folder", f) for f in os.listdir("face_recognition/service_metier/folder")]
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
                detected_persons.add(etudiant)
                print("img_path = " + imagePath + ' --> ' + etudiant.user.username)

    return detected_persons

