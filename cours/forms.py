
#   EQUIPE  : Univit
#   @author : Koutar OUBENADDI et OUGOUD Khadija

from dataclasses import fields
from pyexpat import model
from django import forms

from cours.models import Chapitre, Document, Image, Modele3D, Traitement, File
from module.models import ElementModule
from users.models import Professeur


def get_prof_id(request):
    professeur = Professeur.objects.filter(
        user_id=request.user.id).first()
    return professeur


class ChapitreForm(forms.ModelForm):

    class Meta:
        model = Chapitre
        fields = (
            'libelle',
            'description',
            'image',
            'element_module',
        )
        labels = {
            'libelle': 'Nom du chapitre',
            'description': 'Description du chapitre',
            'image': 'Image',
            'element_module': 'Element de module'
        }
        widgets = {
            'libelle': forms.TextInput(attrs={'placeholder': 'Nom du chapitre',
                                              'class': 'form-control',
                                              }),
            'description': forms.Textarea(attrs={'placeholder': 'Description du chapitre',
                                                 'class': 'form-control',
                                                 'cols': 80, 'rows': 5
                                                 }),
            # 'element_module': forms.ChoiceField(choices="hi")
        }

    def __init__(self, *args, **kwargs):
        # if kwargs.__contains__("request"):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields['libelle'].label = ''
        self.fields['description'].label = ''
        self.fields['image'].label = ''
        self.fields['element_module'].label = ''
        self.fields['element_module'].required = False
        self.fields['element_module'].queryset = ElementModule.objects.filter(
            prof_id=get_prof_id(self.request))


CHOICES = [('pdf', 'pdf'), ('docx', 'docx'), ('ppt', 'ppt')]


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = (
            'titre',
            'path',
            'image',

        )
        labels = {
            'titre': 'Nom du Document',
            'path': 'Fichier',
            'image': 'Image',
        }
        widgets = {
            'titre': forms.TextInput(attrs={'placeholder': 'Nom du Document',
                                            'class': 'form-control',
                                            }),

            # 'type': forms.RadioSelect(choices=CHOICES
            #                                      #   , attrs={'class': 'custom-control-input'}
            #                                      ),
            'path': forms.ClearableFileInput(attrs={'multiple': False}),

        }

    def __init__(self, *args, **kwargs):
        # if kwargs.__contains__("request"):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields['titre'].label = ''
        self.fields['path'].label = ''
        self.fields['image'].label = ''


class Modele3DForm(forms.ModelForm):
    class Meta:
        model = Modele3D
        fields = {
            'titre_modele3d',
            # 'path_modele3d'
        }
        labels = {
            'titre_modele3d': 'Nom du Modèle 3D'
        }
        widgets = {
            'titre_modele3d': forms.TextInput(attrs={'placeholder': 'Nom du Modèle 3D',
                                                     'class': 'form-control',
                                                     }),
        }

    def __init__(self, *args, **kwargs):
        if kwargs.keys().__contains__("request"):
            self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields['titre_modele3d'].label = ''
        self.fields['titre_modele3d'].required = False


CHOICES = [('image', 'Image'), ('texte', 'Texte'), ('qrcode', 'QR-Code')]


class TraitementForm(forms.ModelForm):
    class Meta:
        model = Traitement
        fields = (
            'titre_traitement',
            'label_traitement',
            'type_traitement',
            'visibilite',
            'modele3D'
        )
        labels = {
            'titre_traitement': 'Titre',
            'label_traitement': 'Type du generateur du modele',
            'type_traitement': 'Label',
            'visibilite': 'Visibilité',
            'modele3D': 'modele3D'
        }
        widgets = {
            'titre_traitement': forms.TextInput(attrs={'placeholder': 'Nom',
                                                       'class': 'form-control',
                                                       }),
            'label_traitement': forms.Textarea(attrs={'placeholder': 'Label',
                                                      'class': 'form-control',
                                                               'cols': 80, 'rows': 3
                                                      }),
            'type_traitement': forms.RadioSelect(choices=CHOICES
                                                 #   , attrs={'class': 'custom-control-input'}
                                                 ),
        }

    def __init__(self, *args, **kwargs):
        if kwargs.keys().__contains__("request"):
            self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields['titre_traitement'].label = ''
        self.fields['label_traitement'].label = ''
        self.fields['visibilite'].label = ''
        self.fields['modele3D'].label = ''
        self.fields['type_traitement'].required = False
        self.fields['label_traitement'].required = False
        self.fields['visibilite'].required = False
        self.fields['modele3D'].required = False
        self.fields["visibilite"].queryset = Professeur.objects.all().exclude(
            id=get_prof_id(self.request).id)
        self.fields["modele3D"].queryset = Modele3D.objects.filter(
            id__in=[val.id for val in Traitement.objects.filter(visibilite=get_prof_id(self.request))])


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = {
            'name_image': 'Nom de l\'Image',
            'path_image': 'Image',
            # 'is_qrcode': ''
        }
        widgets = {
            'name_image': forms.TextInput(attrs={'placeholder': 'Nom de l\'image',
                                                 'class': 'form-control',
                                                 }),
        }

    def __init__(self, *args, **kwargs):
        if kwargs.keys().__contains__("request"):
            self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields['name_image'].label = ''
        self.fields['path_image'].label = ''


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = {
            'path_file': 'Fichier(s)'
        }
        widgets = {
            'path_file': forms.ClearableFileInput(attrs={'multiple': True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['path_file'].label = ''
        self.fields['path_file'].required = False
