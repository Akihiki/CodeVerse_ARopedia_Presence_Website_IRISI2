from django.contrib import admin

from semestre.models import AnneUniversitaire
from .models import Salle, TypeSalle


""" EQUIPE : CODEVERSE
    @author : KANNOUFA FATIMA EZZAHRA
    @author : FIROUD REDA et OUSSAHI SALMA 
"""

admin.site.register(Salle)
admin.site.register(TypeSalle)
admin.site.register(AnneUniversitaire)