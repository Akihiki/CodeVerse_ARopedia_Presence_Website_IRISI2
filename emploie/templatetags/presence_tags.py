from django import template
import markdown
from django.utils.safestring import mark_safe
from face_recognition.service_metier.utils import getImagesFromBackup
from users.models import Professeur

register = template.Library()

# tags
@register.simple_tag
def connected_prof_id(user):
    prof = Professeur.objects.get(user_id=user.id)
    if prof:    
        return prof.id

# template filter
@register.filter(name='presence_filter')
def presenceFilter(presence):
    if presence == 1:
        str = '<span class="badge badge-pill badge-success center"> Présent(e)</span>'
    
    if presence == 0:
        str = '<span class="badge badge-pill badge-danger center"> Absent(e)</span>'
    
    return mark_safe(markdown.markdown(str))


@register.filter(name='photo_filter')
def photoFilter(profile_picture):
    if profile_picture :
        str =f'<img class="rounded-circle " width="50px" src="/{profile_picture}" />'
    
    else:
        str = '<img class="rounded-circle " width="50px" src="/media/avatar-default.png" />'
    
    return mark_safe(markdown.markdown(str))


@register.inclusion_tag('emploie/espace_prof/includes/modals/_backup.html')
def show_images(filiere, niveau, groupe, idSeance):
    images = getImagesFromBackup(filiere, niveau, groupe, idSeance)
    
    return {'images': images}

