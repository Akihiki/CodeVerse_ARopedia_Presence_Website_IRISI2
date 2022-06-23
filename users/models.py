from django.db import models
from django.contrib.auth.models import AbstractUser
# from PIL import Image
from django.core.validators import RegexValidator
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
import datetime
import time


def image_upload_location(instance, filename):
    filebase, extension = filename.split('.')
    now = time.time()
    stamp = datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d-%H-%M-%S')
    return 'img/etudiant/%s.%s' % (str(stamp), extension)


class SessionYearModel(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    objects = models.Manager()


class CustomUser(AbstractUser):
    user_type_data = ((1, "Admin"), (2, "Professeur"), (3, "Etudiant"))
    AbstractUser._meta.get_field('email')._unique = True
    user_type = models.CharField(
        default=1, choices=user_type_data, max_length=10)


class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.admin.username


class Professeur(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    admin = models.ForeignKey(
        Admin, on_delete=models.CASCADE, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    specialite = models.CharField(max_length=45, default="Informatique")
    matricule = models.CharField(max_length=45, default="")
    telephone = models.CharField(max_length=10, default="")
    objects = models.Manager()

    def __str__(self):
        return self.user.username

# UnivIt responsable : ismail errouk


class Students(models.Model):
    cne = models.CharField(max_length=100, default="")
    adresse = models.CharField(max_length=100, default="")
    path_photos = models.CharField(max_length=200, default="")
    telephone = models.CharField(max_length=100, default="")
    code_apogee = models.CharField(max_length=100, default="")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    profile_pic = models.FileField(null=True, upload_to=image_upload_location)
    groupes = models.ManyToManyField('semestre.Groupe', null=True)


# Creating Django Signals

# It's like trigger in database. It will run only when Data is Added in CustomUser model

@receiver(post_save, sender=CustomUser)
# Now Creating a Function which will automatically insert data in Admin, Teacher or Student
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        # Check the user_type and insert the data in respective tables
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        if instance.user_type == 2:
            Professeur.objects.create(user=instance)
        if instance.user_type == 3:
            Students.objects.create(admin=instance,
                                    # course_id=
                                    session_year_id=SessionYearModel.objects.get(
                                        id=1),
                                    address="",
                                    profile_pic="",
                                    gender="")


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    # if instance.user_type == 2:
    #     instance.teacher.save()
    if instance.user_type == 3:
        instance.students.save()

# ---------------------------
# UnivIt responsable : ismail errouk


class Permission(models.Model):
    libelle = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.libelle

# UnivIt responsable : ismail errouk


class Role(models.Model):
    libelle = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    user = models.ManyToManyField(CustomUser)
    permissions = models.ManyToManyField(Permission)

    def __str__(self):
        return self.libelle
