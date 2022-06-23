
""" EQUIPE : CODEVERSE
    @author : KANNOUFA FATIMA EZZAHRA
    @author: FIROUD REDA & OUSSAHI SALMA
"""

from rest_framework import serializers
from emploie.models import Planning, Presence, Seance
from face_recognition.api.serializers import FiliereSerializer
from semestre.models import Groupe, Niveau
from users.models import Students, CustomUser
from rest_framework.serializers import ModelField

#   serialisation   #
class NiveauSerializer(serializers.ModelSerializer):
    filiere = FiliereSerializer()
    class Meta:
        model = Niveau
        fields = '__all__'
 
        
class GroupeSerializer(serializers.ModelSerializer):
    niveau = NiveauSerializer()
    class Meta:
        model = Groupe
        fields = '__all__'
            
        
class PlanningSerializer(serializers.ModelSerializer):
    groupe = GroupeSerializer()
    class Meta:
        model = Planning
        fields = '__all__'        


class SeanceSerializer(serializers.ModelSerializer):
    planning = PlanningSerializer()
    class Meta:
        model = Seance
        fields = '__all__'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    username = ModelField(model_field=CustomUser()._meta.get_field('username'))
    class Meta:
        model = CustomUser
        fields = ('username','id')

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Students
        fields = '__all__'

class PresenceSerializer(serializers.ModelSerializer):
    etudiant = StudentSerializer()
    seance = SeanceSerializer()
    class Meta:
        model = Presence
        fields = '__all__'
        
        





