from django import forms

from emploie.models import Planning, TypeSalle, Salle
#FIROUD REDA et OUSSAHI SALMA
JOURS =(
    ( " "," "),
    ( "monday","monday"),
    ( "tuesday","tuesday"),
    ( "wednesday","wednesday"),
    ( "thursday","thursday"),
    ( "friday","friday"),
    ( "saturday","saturday"),
    ("sunday","sunday"),
)

class PlanningForm(forms.ModelForm):  
    class Meta:     
        model = Planning   
        fields = ['libelle','jour','groupe','salle','heure_debut','heure_fin','professeur','element_module']
        widgets = {
                "jour" : forms.Select(choices = JOURS) 
            } 

class TypeSalleForm(forms.ModelForm):  
    class Meta:     
        model = TypeSalle   
        fields = ['capacite','libelle'] 

class SalleForm(forms.ModelForm):  
    class Meta:     
        model = Salle   
        fields = ['nom_salle','disponible','type_salle'] 