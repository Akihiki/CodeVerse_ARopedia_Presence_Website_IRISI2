# from pyexpat import model
# from attr import fields
# from pyrsistent import field
from rest_framework import serializers

from filiere.models import Etablissement, Filiere
class FiliereSerializer(serializers.ModelSerializer):
    class Meta:
        model=Filiere
        fields='__all__'

class EtablissementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etablissement
        fields='__all__'