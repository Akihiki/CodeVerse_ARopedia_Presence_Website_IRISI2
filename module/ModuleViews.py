
# *@author ABDELHADI MOUZAFIR ALL

from csv import DictReader
from datetime import datetime, date
from modulefinder import Module
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from module.models import *
from semestre.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.decorators import api_view
from module.models import ElementModule, Module, Perequis
from module.serializers import ModuleSerializer, ElementModuleSerializer, PerequisSerializer
from rest_framework.response import Response


@login_required
def add_module(request):
    semestres = Semestre.objects.all()
    return render(request, "modules/add_module_template_no_tree.html", {"semestres": semestres})


@login_required
def add_module_level(request, name_):
    niveau = Niveau.objects.get(nom_niveau=name_.replace('_', ' '))
    semestres = Semestre.objects.filter(niveau=niveau)
    if semestres:
        return render(request, "modules/add_module_template.html", {"semestres": semestres, "filiere": niveau.filiere, "niveau": niveau})
    else:
        messages.error(request, "Ajouter au moins un semestre !")
        return render(request, "modules/add_module_template.html", {"semestres": semestres, "filiere": niveau.filiere, "niveau": niveau})


@login_required
def add_module_save(request):
    if request.method != "POST":
        return HttpResponse("<h2> Get or whatever method is not allowed here </h2>")
    else:
        module_libelle = request.POST.get("module")
        semestre_id = request.POST.get("semestre_id")

        try:
            if semestre_id != "" and isinstance(semestre_id, str):
                semestre = Semestre.objects.get(id=semestre_id)
                if module_libelle != "" and isinstance(module_libelle, str) and NotcontainsNumber(module_libelle):
                    course = Module.objects.create(
                        libelle_module=module_libelle, semestre=semestre)
                    course.save()
                    messages.success(
                        request, "Le module est ajouté avec succès !")
                else:
                    messages.error(
                        request, "Nom de module n'est pas valide , doit être comme : 'Analyse'")
                return HttpResponseRedirect(reverse(add_module_level,  kwargs={'name_': semestre.niveau.nom_niveau}))
            else:
                messages.error(request, "Veuillez avoir au moins un semestre")
                return HttpResponseRedirect(reverse(display_levels,  kwargs={'name_': request.POST.get('filiere_')}))
        except:
            messages.error(request, "Echec d'ajout du module !")
            return HttpResponseRedirect(reverse(display_levels,  kwargs={'name_': request.POST.get('filiere_')}))


@login_required
def add_element_module_level(request, name_):
    niveau = Niveau.objects.get(nom_niveau=name_.replace('_', ' '))
    semestre = Semestre.objects.filter(niveau=niveau)
    modules = Module.objects.filter(semestre__in=semestre)
    elements_module = ElementModule.objects.values('responsable')
    responsables = Professeur.objects.exclude(id__in=elements_module)
    profs = Professeur.objects.all()
    prerequis = ElementModule.objects.all()
    # return HttpResponse(profs)
    if modules.exists():
        return render(request, "modules/add_elem_module_template.html", {"profs": profs, "modules": modules, "element_modules": prerequis, "niveau": niveau, "filiere": niveau.filiere, "responsables": responsables})
    else:
        messages.error(request, "Ajoutez au moins un module ")
        return render(request, "modules/add_elem_module_template.html", {"profs": profs, "modules": modules, "element_modules": prerequis, "niveau": niveau, "filiere": niveau.filiere, "responsables": responsables})


@login_required
def add_element_module_save(request):
    if request.method != "POST":
        return HttpResponse("<h2> Get or whatever method is not allowed here </h2>")
    else:
        libelle_element_module = request.POST.get("libelle_element_module")
        module_id = request.POST.get("module_id")
        prerequis_id = request.POST.getlist("prerequis_id")
        volumeHoraire = request.POST.get("volumeHoraire")
        objectif = request.POST.get("objectif")
        prof_id = request.POST.getlist("prof")
        responsable = request.POST.get("responsable")
        niveau = request.POST.get("niveau")
        try:

            if libelle_element_module != "" and isinstance(libelle_element_module, str) and volumeHoraire != "" and objectif != "" and prof_id != [] and responsable != "":
                module = Module.objects.get(id=module_id)
                respo = Professeur.objects.get(id=responsable)
                element_module = ElementModule.objects.create(libelle_element_module=libelle_element_module, volumeHoraire=volumeHoraire,
                                                              objectif=objectif,
                                                              module=module, responsable=respo)

                for pr in prof_id:
                    prof = Professeur.objects.get(id=pr)
                    element_module.prof_id.add(prof)
                    element_module.save()

                for preq in prerequis_id:
                    preqd = ElementModule.objects.get(id=int(preq))
                    d = Perequis.objects.create(
                        element_module_id=element_module, prerequis_id=preqd)
                    d.save()

                messages.success(
                    request, "L'élément de module est ajouté avec succès !")

            else:
                messages.error(
                    request, "Veuillez remplir toutes les champs !")

            return HttpResponseRedirect(reverse(add_element_module_level,  kwargs={'name_': niveau}))
        except:

            messages.error(
                request, "Echec au niveau d'ajout de l'element de module ! ")
            return HttpResponseRedirect(reverse(add_element_module_level,  kwargs={'name_': niveau}))


@login_required
def edit_element_module_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method is Not Allowed</h2>")
    else:
        elem_module_id = request.POST.get("elem_module_id")
        libelle_element_module = request.POST.get("libelle_element_module")
        module_id = request.POST.get("module_id")
        prerequis_id = request.POST.getlist("prerequis_id")
        volumeHoraire = request.POST.get("volumeHoraire")
        objectif = request.POST.get("objectif")
        prof_id = request.POST.getlist("prof")
        module = Module.objects.get(id=module_id)
        responsable = request.POST.get("responsable")
        niveau = request.POST.get("niveau")

        try:
            if libelle_element_module != "" and isinstance(libelle_element_module, str) and volumeHoraire != "" and objectif != "" and prof_id != [] and responsable != "":
                respo = Professeur.objects.get(id=responsable)
                element_module = ElementModule.objects.filter(id=elem_module_id).update(libelle_element_module=libelle_element_module, volumeHoraire=volumeHoraire,
                                                                                        objectif=objectif,
                                                                                        module=module, responsable=respo)
                elem = ElementModule.objects.get(id=elem_module_id)
                elem.prof_id.clear()

                for pr in prof_id:
                    prof = Professeur.objects.get(id=pr)
                    elem.prof_id.add(prof)
                    elem.save()

                Perequis.objects.filter(element_module_id=elem).delete()

                for preq in prerequis_id:
                    preqd = ElementModule.objects.get(id=int(preq))
                    d = Perequis.objects.create(
                        element_module_id=elem, prerequis_id=preqd)
                    d.save()

                messages.success(
                    request, "L'élément de module est modifié avec succès")
                return HttpResponseRedirect(reverse(manage_elem_modules))
            else:
                messages.error(
                    request, "Veuillez remplir toutes les champs !")
                return HttpResponseRedirect(reverse(edit_element_module_level, kwargs={'name_': module.semestre.niveau.nom_niveau, "id_": elem_module_id}))

        except:

            messages.error(
                request, "Echecc de mise à jour")
            return HttpResponseRedirect(reverse(edit_element_module_level, kwargs={'name_': module.semestre.niveau.nom_niveau, "id_": elem_module_id}))


@login_required
def edit_module_save(request):
    if request.method != "POST":
        return HttpResponse("<h2> Get or whatever method is not allowed here </h2>")
    else:
        module_libelle = request.POST.get("module")
        semestre_id = request.POST.get("semestre_id")
        module_id = request.POST.get("module_id")
        semestre = Semestre.objects.get(id=semestre_id)
        try:
            if module_libelle != "" and isinstance(module_libelle, str) and NotcontainsNumber(module_libelle):
                course = Module.objects.get(id=module_id)
                course.libelle_module = module_libelle
                course.semestre = semestre
                course.save()
                messages.success(
                    request, "Le module est modifié avec succès !")
                return HttpResponseRedirect(reverse(manage_modules))
            else:
                messages.error(
                    request, "Nom de module n'est pas valide , doit être comme : 'Analyse'")
                return HttpResponseRedirect(reverse(edit_module,  kwargs={'name_': semestre.niveau.nom_niveau, 'id_': module_id}))
        except:
            messages.error(request, "Echecc de mise à jour !")
            return HttpResponseRedirect(reverse(edit_module,  kwargs={'name_': semestre.niveau.nom_niveau, 'id_': module_id}))


@login_required
def manage_modules(request):
     
    modules = Module.objects.all().order_by('-created_at')
    semestres = Semestre.objects.filter(id=4444)
    niveaux = Niveau.objects.filter(id=4444)
    filieres = Filiere.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(modules, 5)
    try:
        modules_ = paginator.page(page)
    except PageNotAnInteger:
        modules_ = paginator.page(1)
    except EmptyPage:
        modules_ = paginator.page(paginator.num_pages)

    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        print("Loading  data")
        for row in DictReader(open("media/"+filename)):
            print(row)
            level = Niveau.objects.get(nom_niveau=row['niveau'])
            sem= Semestre.objects.filter(libelle_semestre=row['semestre']).get(niveau=level)
            course = Module.objects.create(
            libelle_module=row['ï»¿module_libelle'], semestre=sem)
            course.save()
        return render(request, "modules/manage_modules.html", {"modules": modules_, "filieres": filieres, "semestres": semestres, "niveaux": niveaux ,  'uploaded_file_url': uploaded_file_url})
    return render(request, "modules/manage_modules.html", {"modules": modules_, "filieres": filieres, "semestres": semestres, "niveaux": niveaux })


def search_module(request):
    query = request.GET.get('q')
    modules = Module.objects.filter(
        libelle_module__icontains=query).order_by('-created_at')
    semestres = Semestre.objects.filter(id=4444)
    niveaux = Niveau.objects.filter(id=4444)
    filieres = Filiere.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(modules, 5)
    try:
        modules_ = paginator.page(page)
    except PageNotAnInteger:
        modules_ = paginator.page(1)
    except EmptyPage:
        modules_ = paginator.page(paginator.num_pages)

    return render(request, "modules/manage_modules.html", {"modules": modules_, "filieres": filieres, "semestres": semestres, "niveaux": niveaux})


@login_required
def search_modules_semestres(request, name_):

    semestres = Semestre.objects.filter(libelle_semestre=name_)
    semestres_ = Semestre.objects.values('libelle_semestre').distinct()
    modules = Module.objects.filter(semestre__in=semestres)
    niveaux = Niveau.objects.all()
    filieres = Filiere.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(modules, 5)
    try:
        modules_ = paginator.page(page)
    except PageNotAnInteger:
        modules_ = paginator.page(1)
    except EmptyPage:
        modules_ = paginator.page(paginator.num_pages)

    return render(request, "modules/manage_modules.html", {"modules": modules_, "filieres": filieres, "semestres": semestres_, "niveaux": niveaux})


@login_required
def search_modules_filiere(request, name_):

    filiere = Filiere.objects.get(nom_filiere=name_)
    filieres = Filiere.objects.all()
    niveaux = Niveau.objects.filter(filiere=filiere)
    semestres = Semestre.objects.filter(niveau__in=niveaux)
    modules = Module.objects.filter(semestre__in=semestres)

    page = request.GET.get('page', 1)

    paginator = Paginator(modules, 5)
    try:
        modules_ = paginator.page(page)
    except PageNotAnInteger:
        modules_ = paginator.page(1)
    except EmptyPage:
        modules_ = paginator.page(paginator.num_pages)

    return render(request, "modules/manage_modules.html", {"modules": modules_, "filieres": filieres, "semestres": semestres, "niveaux": niveaux})


@login_required
def search_modules_niveau(request, name_):

    filieres = Filiere.objects.all()
    niveaux = Niveau.objects.all()
    niveau = Niveau.objects.filter(nom_niveau=name_)
    semestres = Semestre.objects.filter(niveau__in=niveau)
    modules = Module.objects.filter(semestre__in=semestres)

    page = request.GET.get('page', 1)

    paginator = Paginator(modules, 5)
    try:
        modules_ = paginator.page(page)
    except PageNotAnInteger:
        modules_ = paginator.page(1)
    except EmptyPage:
        modules_ = paginator.page(paginator.num_pages)

    return render(request, "modules/manage_modules.html", {"modules": modules_, "filieres": filieres, "semestres": semestres, "niveaux": niveaux})


@login_required
def search_elem_modules_filiere(request, name_):
    filiere = Filiere.objects.get(nom_filiere=name_)
    niveaux = Niveau.objects.filter(filiere=filiere)
    semestres = Semestre.objects.filter(niveau__in=niveaux)
    modules = Module.objects.filter(semestre__in=semestres)
    filieres = Filiere.objects.all()
    elem_modules = ElementModule.objects.filter(
        module__in=modules).order_by('-created_at')
    prerequis = Perequis.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(elem_modules, 5)
    try:
        elem_modules_ = paginator.page(page)
    except PageNotAnInteger:
        elem_modules_ = paginator.page(1)
    except EmptyPage:
        elem_modules_ = paginator.page(paginator.num_pages)

    return render(request, "modules/manage_elem_modules.html", {"elem_modules": elem_modules_, "prerequis": prerequis, "filieres": filieres, "semestres": semestres, "niveaux": niveaux, "modules": modules})


@login_required
def search_elem_modules_niveau(request, name_):
    filieres = Filiere.objects.all()
    niveaux = Niveau.objects.all()
    niveau = Niveau.objects.filter(nom_niveau=name_)
    semestres = Semestre.objects.filter(niveau__in=niveau)
    modules = Module.objects.filter(semestre__in=semestres)
    filieres = Filiere.objects.all()
    elem_modules = ElementModule.objects.filter(
        module__in=modules).order_by('-created_at')
    prerequis = Perequis.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(elem_modules, 5)
    try:
        elem_modules_ = paginator.page(page)
    except PageNotAnInteger:
        elem_modules_ = paginator.page(1)
    except EmptyPage:
        elem_modules_ = paginator.page(paginator.num_pages)

    return render(request, "modules/manage_elem_modules.html", {"elem_modules": elem_modules_, "prerequis": prerequis, "filieres": filieres, "semestres": semestres, "niveaux": niveaux, "modules": modules})


@login_required
def search_elem_modules_semestres(request, name_):
    semestres = Semestre.objects.filter(libelle_semestre=name_)
    semestres_ = Semestre.objects.values('libelle_semestre').distinct()
    modules = Module.objects.filter(semestre__in=semestres)
    niveaux = Niveau.objects.all()
    filieres = Filiere.objects.all()
    elem_modules = ElementModule.objects.filter(
        module__in=modules).order_by('-created_at')
    prerequis = Perequis.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(elem_modules, 5)
    try:
        elem_modules_ = paginator.page(page)
    except PageNotAnInteger:
        elem_modules_ = paginator.page(1)
    except EmptyPage:
        elem_modules_ = paginator.page(paginator.num_pages)

    return render(request, "modules/manage_elem_modules.html", {"elem_modules": elem_modules_, "prerequis": prerequis, "filieres": filieres, "semestres": semestres_, "niveaux": niveaux, "modules": modules})


@login_required
def search_elem_modules_modules(request, name_):
    semestres = Semestre.objects.values('libelle_semestre').distinct()
    modules = Module.objects.filter(libelle_module=name_)
    modules_ = Module.objects.all()
    niveaux = Niveau.objects.all()
    filieres = Filiere.objects.all()
    elem_modules = ElementModule.objects.filter(
        module__in=modules).order_by('-created_at')
    prerequis = Perequis.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(elem_modules, 5)
    try:
        elem_modules_ = paginator.page(page)
    except PageNotAnInteger:
        elem_modules_ = paginator.page(1)
    except EmptyPage:
        elem_modules_ = paginator.page(paginator.num_pages)

    return render(request, "modules/manage_elem_modules.html", {"elem_modules": elem_modules_, "prerequis": prerequis, "filieres": filieres, "semestres": semestres, "niveaux": niveaux, "modules": modules_})


@login_required
def search_elem_module(request):
    semestres = Semestre.objects.filter(id=4444)
    niveaux = Niveau.objects.filter(id=4444)
    filieres = Filiere.objects.all()
    query = request.GET.get('q')
    elem_modules = ElementModule.objects.filter(
        libelle_element_module__icontains=query).order_by('-created_at')
    prerequis = Perequis.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(elem_modules, 5)
    try:
        elem_modules_ = paginator.page(page)
    except PageNotAnInteger:
        elem_modules_ = paginator.page(1)
    except EmptyPage:
        elem_modules_ = paginator.page(paginator.num_pages)

    return render(request, "modules/manage_elem_modules.html", {"elem_modules": elem_modules_, "prerequis": prerequis, "filieres": filieres, "semestres": semestres, "niveaux": niveaux})


@login_required
def manage_elem_modules(request):
    semestres = Semestre.objects.filter(id=4444)
    niveaux = Niveau.objects.filter(id=4444)
    modules = Module.objects.filter(id=4444)
    filieres = Filiere.objects.all()
    elem_modules = ElementModule.objects.all()
    prerequis = Perequis.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(elem_modules, 5)
    try:
        elem_modules_ = paginator.page(page)
    except PageNotAnInteger:
        elem_modules_ = paginator.page(1)
    except EmptyPage:
        elem_modules_ = paginator.page(paginator.num_pages)

    return render(request, "modules/manage_elem_modules.html", {"elem_modules": elem_modules_, "prerequis": prerequis, "filieres": filieres, "semestres": semestres, "niveaux": niveaux, "modules": modules})


@login_required
def delete_module(request, id_):
    try:
        Module.objects.filter(id=id_).delete()
        messages.success(request, "Le module est supprimé avec succès !")
        return HttpResponseRedirect(reverse(manage_modules))
    except:
        messages.error(request, "Echec de la suppression !")
        return HttpResponseRedirect(reverse(manage_modules))


@login_required
def delete_elem_module(request, id_):
    try:
        ElementModule.objects.filter(id=id_).delete()
        messages.success(request, "Le module est supprimé avec succès !")
        return HttpResponseRedirect(reverse(manage_elem_modules))

    except:
        messages.error(request, "Echec de la suppression !")
        return HttpResponseRedirect(reverse(manage_modules))


@login_required
def edit_module(request, name_, id_):

    module = Module.objects.get(id=id_)
    niveau = Niveau.objects.get(nom_niveau=name_)
    semestres = Semestre.objects.filter(niveau=niveau)
    # return HttpResponse(niveau.filiere)
    return render(request, "modules/edit_module_template.html", {"module": module, "semestres": semestres, "filiere": niveau.filiere, "niveau": niveau})


@login_required
def display_majors(request):
    filieres = Filiere.objects.all()

    return render(request, "modules/filieres_template.html", {"filieres": filieres})


@login_required
def display_levels(request, name_):
    filiere = Filiere.objects.get(nom_filiere=name_)
    niveaux = Niveau.objects.filter(filiere=filiere)
    if niveaux:
        return render(request, "modules/niveau_template.html", {"filiere": filiere, "niveaux": niveaux})
    else:
        messages.error(request, "Ajouter au moins un niveau")
        return render(request, "modules/niveau_template.html", {"filiere": filiere, "niveaux": niveaux})


@login_required
def edit_element_module_level(request, name_, id_):
    niveau = Niveau.objects.get(nom_niveau=name_)
    semestre = Semestre.objects.filter(niveau=niveau)
    modules = Module.objects.filter(semestre__in=semestre)
    profs = Professeur.objects.all()
    prerequis = ElementModule.objects.all()
    prerequis_ = Perequis.objects.filter(element_module_id=id_)
    element_module = ElementModule.objects.get(id=id_)
    elements_module = ElementModule.objects.exclude(
        id=id_).values('responsable')
    responsables = Professeur.objects.exclude(id__in=elements_module)

    # return HttpResponse(element_module)
    return render(request, "modules/edit_elem_module_template.html", {"profs": profs, "modules": modules, "element_modules": prerequis, "niveau": niveau, "filiere": niveau.filiere, "element": element_module, "prerequis": prerequis_, "responsables": responsables})


def NotcontainsNumber(value):
    for character in value:
        if character.isdigit():
            return False
    return True

    """@author
        Aminatou
    """


@api_view(['GET'])
def liste_modules(request):
    try:
        mod = Module.objects.all()
        serializer = ModuleSerializer(mod, many=True)
        return Response(serializer.data)
    except Module.DoesNotExist:
        return Response([])


@api_view(['GET'])
def liste_ElementModule(request):
    try:
        element = ElementModule.objects.all()
        serializer = ElementModuleSerializer(element, many=True)
        return Response(serializer.data)
    except Module.DoesNotExist:
        return Response([])


@api_view(['GET'])
def liste_Perequis(request):
    try:
        perequis = Perequis.objects.all()
        serializer = PerequisSerializer(perequis, many=True)
        return Response(serializer.data)
    except Module.DoesNotExist:
        return Response([])
