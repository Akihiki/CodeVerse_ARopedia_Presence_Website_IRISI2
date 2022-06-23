from django import forms
from django.forms import Form
from users.models import *


class DateInput(forms.DateInput):
    input_type = "date"


class AddStudentForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = ['user', 'admin','cne', 'adresse', 'telephone', 'path_photos', 'code_apogee']
        labels = {
            'admin': 'Admin',
            'user': 'User',
            'cne': 'CNE',
            'adresse': 'Adresse',
            'telephone': 'Telephone',
            'path_photos': 'Path Photos',
            'code_apogee': 'Code Apogee',

        }

    def __init__(self, *args, **kwargs):
        super(AddStudentForm, self).__init__(*args, **kwargs)


class EditStudentForm(forms.Form):
    adresse = forms.CharField(label="Adresse", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    cne = forms.CharField(label="C.N.E", max_length=10, widget=forms.TextInput(attrs={"class": "form-control"}))
    path_photos = forms.CharField(label="Path Photos", max_length=10,
                                  widget=forms.TextInput(attrs={"class": "form-control"}))
    telephone = forms.CharField(label="Telephone", max_length=10,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    code_apogee = forms.CharField(label="Code Appoge", max_length=10,
                                  widget=forms.TextInput(attrs={"class": "form-control"}))
    # For Displaying Courses

    # # form des Etudiants
    # class EtudiantForm(forms.ModelForm):
    #     class Meta:
    #         model = Etudiant
    #         fields = ['user', 'cne', 'adresse', 'telephone', 'path_photos', 'code_apogee']
    #         labels = {
    #             'user': 'User',
    #             'cne': 'CNE',
    #             'adresse': 'Adresse',
    #             'telephone': 'Telephone',
    #             'path_photos': 'Path Photos',
    #             'code_apogee': 'Code Apogee',
    #
    #         }
    #
    #     def __init__(self, *args, **kwargs):
    #         super(EtudiantForm, self).__init__(*args, **kwargs)
    #
    # DEMO_CHOICES = (
    #     ("1", "Naveen"),
    #     ("2", "Pranav"),
    #     ("3", "Isha"),
    #     ("4", "Saloni"),
    # )
    #
    # def get_demo_choices():
    #     permissions = Permission.objects.all()
    #     list_permissions = []
    #     for permission in permissions:
    #         list_permissions.append((permission.id, permission.libelle))
    #     return list_permissions
    #
    # class GeeksForm(forms.Form):
    #     geeks_field = forms.MultipleChoiceField(choices=get_demo_choices)
