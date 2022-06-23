from django.forms import ModelForm
from ..models import Semestre


class SemestreForm(ModelForm):

    class Meta:
        model = Semestre
        fields = ('libelle_semestre', 'niveau')
        labels = {
            'libelle_semestre': 'Libelle semestre',
            'niveau': 'niveau semestre'
        }

    def __init__(self, *args, **kwargs):
        super(SemestreForm, self).__init__(*args, **kwargs)
        self.fields['niveau'].empty_label = "Select"

