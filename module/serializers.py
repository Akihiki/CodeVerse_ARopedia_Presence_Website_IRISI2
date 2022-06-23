from rest_framework import serializers
from module.models import Module, ElementModule, Perequis

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Module
        fields='__all__'

class ElementModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model=ElementModule
        fields='__all__'

class PerequisSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Perequis
        fields='__all__'