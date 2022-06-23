from django import forms

from semestre.models import Groupe
from users.models import Permission
# UnivIt responsable : ismail errouk
DEMO_CHOICES = (
    ("1", "Naveen"),
    ("2", "Pranav"),
    ("3", "Isha"),
    ("4", "Saloni"),
)


def get_demo_choices():
    permissions = Permission.objects.all()
    list_permissions = []
    for permission in permissions:
        list_permissions.append((permission.id, permission.libelle))
    return list_permissions


class GeeksForm(forms.Form):
    Permissions = forms.MultipleChoiceField(choices=get_demo_choices)


# ----------Groupes ----------

def get_groupe_choices():
    groupes = Groupe.objects.all()
    list_groupes = []
    for groupe in groupes:
        list_groupes.append((groupe.id, groupe.nom_group))
    return list_groupes


class GroupeListForm(forms.Form):
    Groupes = forms.MultipleChoiceField(choices=get_groupe_choices)