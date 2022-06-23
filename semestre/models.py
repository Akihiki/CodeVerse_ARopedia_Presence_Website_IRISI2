from django.db import models

from filiere.models import Filiere
from users.models import Students


# Create your models here.


class Niveau(models.Model):
    nom_niveau = models.CharField(max_length=100, null=True)
    type_niveau = models.CharField(max_length=100, null=True)
    filiere = models.ForeignKey(Filiere , null=True,  on_delete= models.SET_NULL )

    def __str__(self):
        return self.nom_niveau

class Groupe(models.Model):
    nom_group = models.CharField(max_length=100, null=True)
    niveau = models.ForeignKey(Niveau ,  null=True,  on_delete= models.SET_NULL)
    
    def __str__(self):
        return self.nom_group


class AnneUniversitaire(models.Model):
    group = models.ForeignKey(Groupe , null=True,  on_delete= models.SET_NULL )
    etudiant = models.ForeignKey(Students , null=True,  on_delete= models.SET_NULL)
    libelle = models.CharField(max_length=100, null=True)
    date = models.DateField(null = False )

    def __str__(self):
        return self.libelle


class Semestre(models.Model):
    libelle_semestre = models.CharField(max_length=100, null=True) 
    niveau = models.ForeignKey(Niveau ,  null=True , on_delete= models.SET_NULL )
    
    def __str__(self):
        return self.libelle_semestre