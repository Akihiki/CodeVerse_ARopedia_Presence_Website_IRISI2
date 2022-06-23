from django import forms
from ..models import Niveau


class NiveauForm(forms.ModelForm):

    class Meta:
        model = Niveau
        fields = ('nom_niveau', 'type_niveau', 'filiere')
        labels = {
            'nom_niveau': 'Nom Niveau',
            'type_niveau': 'Type Niveau'
        }

    def __init__(self, *args, **kwargs):
        super(NiveauForm, self).__init__(*args, **kwargs)
        self.fields['filiere'].empty_label = "Select"
        # self.fields['filiere'].required = True
