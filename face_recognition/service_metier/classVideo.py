
""" EQUIPE : CodeVerse et ARopedia
    @authors :  + KANNOUFA F. EZZAHRA
                + MOUZAFIR ABDELHADI
"""

import cv2, os
from users.models import Students

path_dataset = "face_recognition/service_metier/dataset/"

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

class VideoCamera():
	def __init__(self,id):
		self.id=id
		self.video = cv2.VideoCapture(2)
		self.count = 0 
  
	def __del__(self):
		self.video.release()
  
	def get_frame(self):
		success, image = self.video.read()
		faceCascade = cv2.CascadeClassifier("face_recognition/service_metier/models/haarcascade_frontalface_default.xml")
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		faces_detected = faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5,minSize= (30,30))
  		
    	# données de l'étudiant
		etudiant = Students.objects.get(pk=self.id)
  
		# créer un dossier pour cet étudiant
		folder_name = path_dataset + "Etudiant_" + etudiant.user.last_name + "_" + etudiant.user.first_name  + '/'
		assure_path_exists(folder_name)
  
		
		# enregistrer les images de l'étudiant dans le dossier
		for (x, y, w, h) in faces_detected:
			cv2.rectangle(image, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2)
			self.count += 1
			cv2.imwrite(folder_name + "Etudiant." + str(etudiant.id) + '.' + str(self.count) +".jpg", gray[y:y+h,x:x+w])
   
		frame_flip = cv2.flip(image,1)
		ret, jpeg = cv2.imencode('.jpg', frame_flip)
  
		return jpeg.tobytes()

