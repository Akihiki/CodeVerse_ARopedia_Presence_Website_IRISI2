from django import forms

from users.models import *

# UnivIt responsable : ismail errouk
class AddPermissionForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ['libelle', 'description']
        labels = {
            'libelle': 'Libelle',
            'description': 'Description',

        }

    def __init__(self, *args, **kwargs):
        super(AddPermissionForm, self).__init__(*args, **kwargs)

# UnivIt responsable : ismail errouk
class EditPermissionForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ['libelle', 'description']
        labels = {
            'libelle': 'Libelle',
            'description': 'Description',

        }

    def __init__(self, *args, **kwargs):
        super(EditPermissionForm, self).__init__(*args, **kwargs)
