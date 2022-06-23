import datetime
import time
from django.db import models

# Create your models here.
def upload_location(instance, filename):
        filebase, extension = filename.split('.')
        now = time.time()
        stamp = datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d-%H-%M-%S')
        return 'filiere_images/%s.%s' % (str(stamp), extension)
class Filiere(models.Model):
    nom_filiere = models.CharField(max_length=30)
    logo = models.ImageField(upload_to=upload_location)
    def __str__(self):
        return self.nom_filiere
    