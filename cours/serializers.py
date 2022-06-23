
#   EQUIPE  : Univit
#   @author : Koutar OUBENADDI et OUGOUD Khadija

from cours.models import *
from rest_framework import serializers


class ChapitreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapitre
        fields = ['id', 'libelle', 'description', 'image']


class TraitementSerializerImage(serializers.ModelSerializer):
    class Meta:
        model = Traitement
        # fields = '__all__'
        fields = ['id', 'titre_traitement']

class DocumentSerializerImage(serializers.ModelSerializer):
    class Meta:
        model = Document
        # fields = '__all__'
        fields = ['id', 'titre','image','path']

class Modele3DSerializerImage(serializers.ModelSerializer):
    class Meta:
        model = Modele3D
        fields = ['path_modele3d']


class FileSerializerImage(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['path_file']


class ImageSerializerImage(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['path_image']


class TraitementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Traitement
        fields = '__all__'


class Modele3DSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modele3D
        fields = '__all__'


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['path_file']


