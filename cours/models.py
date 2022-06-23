
#   EQUIPE  : Univit
#   @author : Koutar OUBENADDI et OUGOUD Khadija et ERROUK Ismail et ETTAFSSAOUI Youssef

from django.db import models
from pymysql import NULL
from module.models import ElementModule
import datetime
import time
# from PIL import Image

from users.models import Professeur


def upload_location(instance, filename):
    filebase, extension = filename.split('.')
    now = time.time()
    stamp = datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d-%H-%M-%S')
    return 'img/cours/chapitre_images/%s.%s' % (str(stamp), extension)


def document_image_upload_location(instance, filename):
    filebase, extension = filename.split('.')
    now = time.time()
    stamp = datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d-%H-%M-%S')
    return 'img/cours/document_images/%s.%s' % (str(stamp), extension)


def document_file_upload_location(instance, filename):
    filebase, extension = filename.split('.')
    now = time.time()
    stamp = datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d-%H-%M-%S')
    return 'img/cours/document_files/%s.%s' % (str(stamp), extension)


def model_location(modelName):
    now = time.time()
    stamp = datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d-%H-%M-%S')
    return 'img/cours/modeles_3d/%s-%s' % (modelName, str(stamp))


def model_image_location(instance, filename):
    filebase, extension = filename.split('.')
    now = time.time()
    stamp = datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d-%H-%M-%S')
    return 'img/cours/modeles_3d_images/%s.%s' % (str(stamp), extension)


def file_upload_location(instance, filename):
    modele3d = instance.modele3D.path_modele3d
    return '%s/%s' % (modele3d, filename)


class Chapitre(models.Model):
    libelle = models.CharField(max_length=40, null=False)
    description = models.CharField(max_length=250, null=True)
    image = models.ImageField(
        upload_to=upload_location, default='/img/cours/folder-files-and-folders-svgrepo-com.svg')
    element_module = models.ForeignKey(
        ElementModule, null=True,  on_delete=models.SET_NULL)
    professeur = models.ForeignKey(
        Professeur, null=False, on_delete=models.CASCADE)
    # visibilite
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    # def year_created(self):
    #     return self.created_at.strftime('%Y')


class Document(models.Model):
    titre = models.CharField(max_length=40, null=False)
    type = models.CharField(max_length=20, null=False)
    path = models.FileField(
        upload_to=document_file_upload_location, null=False, max_length=255)
    image = models.ImageField(
        upload_to=document_image_upload_location, default=NULL)
    chapitre = models.ForeignKey(
        Chapitre, null=False,  on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)


class Modele3D(models.Model):
    titre_modele3d = models.CharField(max_length=40, null=False)
    path_modele3d = models.CharField(max_length=100, null=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre_modele3d


class Image(models.Model):
    name_image = models.CharField(
        max_length=30, null=False, default='Sans Nom')
    is_qrcode = models.BooleanField(default=False)
    path_image = models.FileField(
        upload_to=model_image_location, null=False, default=NULL)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)


class Traitement(models.Model):
    titre_traitement = models.CharField(max_length=40, null=False)
    label_traitement = models.CharField(max_length=100, null=True, blank=True)
    type_traitement = models.CharField(max_length=25, null=False)
    chapitre = models.ForeignKey(
        Chapitre, null=False,  on_delete=models.CASCADE)
    image = models.ForeignKey(
        Image, null=True, blank=True,  on_delete=models.SET_NULL, default=NULL)
    modele3D = models.ForeignKey(
        Modele3D, null=False,  on_delete=models.CASCADE)
    visibilite = models.ManyToManyField(Professeur)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)


class File(models.Model):
    # path = models.CharField(max_length=100,null = False )
    modele3D = models.ForeignKey(
        Modele3D, null=False,  on_delete=models.CASCADE)
    path_file = models.FileField(
        upload_to=file_upload_location, null=False, max_length=255)
    # file = models.FileField(upload_to=file_upload_location(foldername=get_modele_3d(modele3D)),null = False )
    # file = models.FileField(null = False )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
