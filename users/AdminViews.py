import csv
import io
import logging
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage  # To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from semestre.models import Groupe
from filiere.models import Filiere, Etablissement
from emploie.models import Planning
from module.models import ElementModule, Module
from users.models import Admin, CustomUser, Professeur, Students

# Page Administrateur - Statistiques & Routes : Ettafssaoui Youssef
def admin_home(request):
    all_student_count = Students.objects.all().count()
    all_filiere_count = Filiere.objects.all().count()
    all_professeur_count = Professeur.objects.all().count()
    all_etablissements_count = Etablissement.objects.all().count()
    all_emploie_count = Planning.objects.all().count()
    all_module_count = Module.objects.all().count()
    all_elem_modules_count = ElementModule.objects.all().count()
    all_users_count = CustomUser.objects.all().count()
    context = {
        "all_student_count": all_student_count,
        "all_professeur_count": all_professeur_count,
        "all_users_count" : all_users_count,
        "all_filiere_count": all_filiere_count,
        "all_etablissements_count": all_etablissements_count,
        "all_emploie_count": all_emploie_count,
        "all_module_count": all_module_count,
        "all_elem_modules_count": all_elem_modules_count
    }
    return render(request, "admin/home_content.html", context)

# Gestion des Utilisateurs : Ettafssaoui Youssef
def manage_users(request):
    users = CustomUser.objects.all().order_by('-date_joined')
    all_users_count = CustomUser.objects.all().count()
    page = request.GET.get('page', 1)
    pag = Paginator(users,100)
    try:
        ausers = pag.page(page)
    except PageNotAnInteger:
        ausers = pag.page(1)
    except EmptyPage:
        ausers = pag.page(pag.num_pages)
    context = {
        "users": ausers,
        "all_users_count": all_users_count
    }
    return render(request, "admin/manage_users_template.html", context)

# Importer des Utilisateurs par un fichier CSV : Ettafssaoui Youssef
def upload_csv(request):
    data = {}
    if "GET" == request.method:
        return render(request, "admin/upload_csv.html", data)
    try:
        csv_file = request.FILES["csv_file"]
        
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return HttpResponseRedirect(reverse("upload_csv"))
        
        if csv_file.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("upload_csv"))
        file_data = csv_file.read().decode("utf-8")		
        lines = file_data.split("\n")
        for line in lines:						
            fields = line.split(",")
            data_dict = {}
            data_dict["email"] = fields[0]
            data_dict["password"] = fields[1]
            data_dict["username"] = fields[2]
            data_dict["first_name"] = fields[3]
            data_dict["last_name"] = fields[4]
            data_dict["user_type"] = fields[5]
            try:
                form = CustomUser(data_dict)
                if form.is_valid():
                    form.save()				
                else:
                    logging.getLogger("error_logger").error(form.errors.as_json())												
            except Exception as e:
                logging.getLogger("error_logger").error(repr(e))					
                pass
    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        messages.error(request,"Unable to upload file. "+repr(e))
        
    return HttpResponseRedirect(reverse("upload_csv"))

# Ajout du Professeur : Ettafssaoui Youssef
def add_professeur(request):
    admins = Admin.objects.all()
    return render(request, "admin/add_professeur_template.html",{'admins': admins})

# Ajout du Professeur : Ettafssaoui Youssef
def add_professeur_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method !")
        return redirect('add_professeur')
    else:
        admin = Admin.objects.get(id=request.POST['select_admin'])
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        specialite = request.POST.get('specialite')
        matricule = request.POST.get('matricule')
        telephone = request.POST.get('telephone')
        try:
            user = CustomUser()
            user.user_type = 2
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.password = password
            user.save()
            professeur = Professeur.objects.get(user=user)
            professeur.specialite = specialite
            professeur.matricule = matricule
            professeur.telephone = telephone
            professeur.user = user
            professeur.save()
            messages.success(request, "Professeur ajouté avec succés !")
            return redirect('add_professeur')
        except:
            messages.error(request, "Impossible d'ajouter le Professeur !")
            return redirect('add_professeur')

# Gestion du Professeur : Ettafssaoui Youssef
def manage_professeur(request):
    professeurs = Professeur.objects.all().order_by('-created_at')
    all_professeur_count = Professeur.objects.all().count()
    page = request.GET.get('page', 1)
    pag = Paginator(professeurs, 8)
    try:
        aprofesseurs = pag.page(page)
    except PageNotAnInteger:
        aprofesseurs = pag.page(1)
    except EmptyPage:
        aprofesseurs = pag.page(pag.num_pages)
    context = {
        "professeurs": aprofesseurs,
        "all_professeur_count": all_professeur_count
    }
    return render(request, "admin/manage_professeur_template.html", context)

# Modification du Professeur : Ettafssaoui Youssef
def edit_professeur(request, professeur_id):
    professeur = Professeur.objects.get(user=professeur_id)

    context = {
        "professeur": professeur,
        "id": professeur_id
    }
    return render(request, "admin/edit_professeur_template.html", context)

# Modification du Professeur : Ettafssaoui Youssef
def edit_professeur_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        professeur_id = request.POST.get('professeur_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        specialite = request.POST.get('specialite')
        matricule = request.POST.get('matricule')
        telephone = request.POST.get('telephone')

        try:
            # INSERTING into Customuser Model
            user = CustomUser.objects.get(id=professeur_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            # INSERTING into Professeur Model
            professeur_model = Professeur.objects.get(user=professeur_id)
            professeur_model.specialite = specialite
            professeur_model.matricule = matricule
            professeur_model.telephone = telephone
            professeur_model.save()

            messages.success(request, "professeur Updated Successfully !")
            return redirect('/edit_professeur/'+professeur_id)

        except:
            messages.error(request, "Failed to Update professeur !")
            return redirect('/edit_professeur/'+professeur_id)

# Supressions du Professeur : Ettafssaoui Youssef
def delete_professeur(request, professeur_id):
    professeur = Professeur.objects.get(user=professeur_id)
    try:
        professeur.delete()
        messages.success(request, "Professeur Supprimé avec succès !")
        return redirect('manage_professeur')
    except:
        messages.error(request, "Erreur lors la suppression du Professeur !")
        return redirect('manage_professeur')

# Admin Profile : Ettafssaoui Youssef
def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)

    context = {
        "user": user
    }
    return render(request, 'admin/admin_profile.html', context)

# Modification d'Admin Profile : Ettafssaoui Youssef
def admin_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('admin/admin_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('admin/admin_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('admin/admin_profile')


def professeur_profile(request):
    pass


def student_profile(requtest):
    pass
