from django import forms
from ..models import Groupe


class GroupeForm(forms.ModelForm):

    class Meta:
        model = Groupe
        fields = ('nom_group', 'niveau')
        labels = {
            'nom_group': 'Nom Groupe',
            'niveau': 'Niveau'
        }

    def __init__(self, *args, **kwargs):
        super(GroupeForm, self).__init__(*args, **kwargs)
        self.fields['niveau'].empty_label = "Select"
        self.fields['niveau'].required = True