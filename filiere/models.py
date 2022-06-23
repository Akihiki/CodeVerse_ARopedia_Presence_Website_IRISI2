from django.db import models
import datetime
import time
from os import path
# Create your models here.
def upload_location_filiere(instance, filename):
        filebase, extension = path.splitext(filename)
        now = time.time()
        stamp = datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d-%H-%M-%S')
        return 'filiere_images/%s.%s' % (str(stamp), extension)
def upload_location_etablissement(instance, filename):
        filebase, extension = path.splitext(filename)
        now = time.time()
        stamp = datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d-%H-%M-%S')
        return 'etablissement_images/%s.%s' % (str(stamp), extension)


class Etablissement(models.Model):
    nom = models.CharField(max_length=100, null=True)
    adresse = models.CharField(max_length=100, null=True)
    telephone = models.CharField(max_length=20, null=True)
    niveau=models.CharField(max_length=100,null=True)
    website=models.URLField(max_length=100,null=True)
    email=models.EmailField(max_length=100,null=True)
    logo = models.ImageField(upload_to=upload_location_etablissement)
    def __str__(self):
        return self.nom


class Filiere(models.Model):
    nom_filiere = models.CharField(max_length=30)
    logo = models.ImageField(upload_to=upload_location_filiere)
    etablissement = models.ForeignKey(Etablissement , null=True,  on_delete= models.CASCADE)
    def __str__(self):
        return self.nom_filiere
