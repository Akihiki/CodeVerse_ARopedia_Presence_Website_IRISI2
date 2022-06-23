

#   EQUIPE  : Univit
#   @author : Koutar OUBENADDI et OUGOUD Khadija

from PIL import Image, ImageDraw
import imghdr
import os
import cv2
from pydoc import doc
import time
import datetime
from cv2 import QRCodeDetector
import django
from django.db.models import Q
from scipy.fft import ifftn
from cours.serializers import *
from functools import reduce
from users.models import Professeur
from semestre.models import Niveau, Semestre
from module.models import ElementModule, Module
from filiere.models import Filiere
from cours.models import Chapitre, Document, Modele3D, Traitement, File, Image
from django.db.models import Count
from django.db.models.functions import ExtractYear
from django.contrib.auth.decorators import login_required
from cours.forms import *
from pymysql import NULL
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
import json
from django.core.serializers import serialize
from distutils.command import check
import sys
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import FileSerializer, Modele3DSerializer, TraitementSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from django.shortcuts import render, redirect

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseNotFound

import qrcode
from io import *

NoneType = type(None)

# from django.core.files import File


@api_view(['POST'])
def get_traitement(request):
    Qrr = qrcode.make("hhh")
    try:
        # returns the first modele3d that contains at least one of desired words
        str = request.data.get('text')
        chunks = str.split(',')
        mylist = [f",{s}," for s in chunks]
        # try:
        Traitements = Traitement.objects.filter(chapitre=request.data.get('chapitre_id')).filter(
            reduce(lambda x, y: x | y, [Q(label_traitement__contains=word) for word in mylist]))
        print(mylist)
        print(len(Traitements))
        if(len(Traitements) <= 0):
            return Response([{'erreur ': 'pas de modele 3d associé'}], status=404)
        else:

            Modele3Ds = Modele3D.objects.filter(
                id=Traitements[0].modele3D_id).first()
            Files = File.objects.filter(modele3D=Modele3Ds.id).first()

            serializer = FileSerializer(Files, many=False)
            return Response(serializer.data)
    except File.DoesNotExist:
        return Response([{'erreur ': 'pas de modele 3d associé'}], status=404)


@login_required
def chapitres_list(request):
    search_by = NoneType
    professeur = Professeur.objects.filter(user_id=request.user.id).first()

    new_chapitre = ChapitreForm(request=request)

    element_modules = ElementModule.objects.filter(prof_id=professeur)
    modules = Module.objects.filter(
        id__in=element_modules.values_list('module_id'))
    semestres = Semestre.objects.filter(
        id__in=modules.values_list('semestre_id'))
    niveaux = Niveau.objects.filter(
        id__in=semestres.values_list('niveau_id'))
    filieres = Filiere.objects.filter(id__in=niveaux.values_list('filiere_id'))

    annees = Chapitre.objects.annotate(year=ExtractYear('created_at'))
    search_chapitre = request.GET.get('search')
    if search_chapitre:
        chapitres = Chapitre.objects.filter((Q(libelle__icontains=search_chapitre) | Q(
            description__icontains=search_chapitre)) & Q(professeur=professeur.id) & Q(deleted=False))
        search_by = " qui contiennent \" " + search_chapitre + " \""
    else:
        chapitres = Chapitre.objects.filter(
            professeur=professeur.id, deleted=False)

    page = request.GET.get('page', 1)
    paginator = Paginator(chapitres, 10)
    try:
        chapitres_page = paginator.page(page)
    except PageNotAnInteger:
        chapitres_page = paginator.page(1)
    except EmptyPage:
        chapitres_page = paginator.page(paginator.num_pages)

    context = {
        "chapitres": chapitres_page,
        "professeur": professeur,
        "filieres": filieres,
        "niveaux": niveaux,
        "element_modules": element_modules,
        "annees": annees,
        "search_by": search_by,
        "new_chapitre": new_chapitre
    }
    return render(request, 'cours/chapitres.html', context)


@login_required
def search_chapitres_by_filiere(request, val):

    new_chapitre = ChapitreForm(request=request)

    professeur = Professeur.objects.filter(user_id=request.user.id).first()

    filieres = Filiere.objects.all()
    filiere = Filiere.objects.filter(nom_filiere=val).first()
    niveaux = Niveau.objects.filter(filiere=filiere)
    semestres = Semestre.objects.filter(niveau__in=niveaux)
    modules = Module.objects.filter(semestre__in=semestres)
    element_modules = ElementModule.objects.filter(
        module__in=modules, prof_id=professeur)
    chapitres = Chapitre.objects.filter(
        element_module__in=element_modules, deleted=False)
    annees = Chapitre.objects.annotate(year=ExtractYear('created_at'))

    search_by = "pour la filière \" "+val + " \""
    search_chapitre = request.GET.get('search')
    if search_chapitre:
        chapitres = Chapitre.objects.filter((Q(libelle__icontains=search_chapitre) | Q(
            description__icontains=search_chapitre)) & Q(professeur=professeur.id) & Q(element_module__in=element_modules) & Q(deleted=False))
        search_by += " qui contiennent \" " + search_chapitre + " \""

    page = request.GET.get('page', 1)
    paginator = Paginator(chapitres, 10)
    try:
        chapitres_page = paginator.page(page)
    except PageNotAnInteger:
        chapitres_page = paginator.page(1)
    except EmptyPage:
        chapitres_page = paginator.page(paginator.num_pages)

    context = {
        "chapitres": chapitres_page,
        "professeur": professeur,
        "filieres": filieres,
        "niveaux": niveaux,
        "element_modules": element_modules,
        "annees": annees,
        "search_by": search_by,
        "new_chapitre": new_chapitre
    }

    return render(request, "cours/chapitres.html", context)


@login_required
def search_chapitres_by_niveau(request, val):

    new_chapitre = ChapitreForm(request=request)

    professeur = Professeur.objects.filter(user_id=request.user.id).first()

    filieres = Filiere.objects.all()
    niveaux = Niveau.objects.all()
    niveau = Niveau.objects.get(nom_niveau=val)
    semestres = Semestre.objects.filter(niveau=niveau)
    modules = Module.objects.filter(semestre__in=semestres)
    element_modules = ElementModule.objects.filter(
        module__in=modules, prof_id=professeur)
    chapitres = Chapitre.objects.filter(
        element_module__in=element_modules, deleted=False)
    annees = Chapitre.objects.annotate(year=ExtractYear('created_at'))

    search_by = "pour le niveau \" "+val + " \""

    search_chapitre = request.GET.get('search')
    if search_chapitre:
        chapitres = Chapitre.objects.filter((Q(libelle__icontains=search_chapitre) | Q(
            description__icontains=search_chapitre)) & Q(professeur=professeur.id) & Q(element_module__in=element_modules) & Q(deleted=False))
        search_by += " qui contiennent \" " + search_chapitre + " \""

    page = request.GET.get('page', 1)
    paginator = Paginator(chapitres, 10)
    try:
        chapitres_page = paginator.page(page)
    except PageNotAnInteger:
        chapitres_page = paginator.page(1)
    except EmptyPage:
        chapitres_page = paginator.page(paginator.num_pages)

    context = {
        "chapitres": chapitres_page,
        "professeur": professeur,
        "filieres": filieres,
        "niveaux": niveaux,
        "element_modules": element_modules,
        "annees": annees,
        "search_by": search_by,
        "new_chapitre": new_chapitre
    }

    return render(request, "cours/chapitres.html", context)


@login_required
def search_chapitres_by_element_module(request, val):

    new_chapitre = ChapitreForm(request=request)

    professeur = Professeur.objects.filter(user_id=request.user.id).first()

    filieres = Filiere.objects.all()
    niveaux = Niveau.objects.all()
    # element_modules = ElementModule.objects.filter(prof_id=professeur)
    element_modules = ElementModule.objects.filter(prof_id=professeur)
    element_module = ElementModule.objects.filter(
        libelle_element_module=val).first()
    chapitres = Chapitre.objects.filter(
        element_module=element_module, deleted=False)
    annees = Chapitre.objects.annotate(year=ExtractYear('created_at'))

    search_by = "pour le module \" "+val + " \""

    search_chapitre = request.GET.get('search')
    if search_chapitre:
        chapitres = Chapitre.objects.filter((Q(libelle__icontains=search_chapitre) | Q(
            description__icontains=search_chapitre)) & Q(professeur=professeur.id) & Q(element_module=element_module) & Q(deleted=False))
        search_by += " qui contiennent \" " + search_chapitre + " \""

    page = request.GET.get('page', 1)
    paginator = Paginator(chapitres, 10)
    try:
        chapitres_page = paginator.page(page)
    except PageNotAnInteger:
        chapitres_page = paginator.page(1)
    except EmptyPage:
        chapitres_page = paginator.page(paginator.num_pages)

    context = {
        "chapitres": chapitres_page,
        "professeur": professeur,
        "filieres": filieres,
        "niveaux": niveaux,
        "element_modules": element_modules,
        "annees": annees,
        "search_by": search_by,
        "new_chapitre": new_chapitre
    }

    return render(request, "cours/chapitres.html", context)


@login_required
def search_chapitres_by_annee(request, val):

    new_chapitre = ChapitreForm(request=request)

    professeur = Professeur.objects.filter(user_id=request.user.id).first()
    # filieres = Filiere.objects.all()
    # niveaux = Niveau.objects.all()
    element_modules = ElementModule.objects.filter(prof_id=professeur)

    modules = Module.objects.filter(
        id__in=element_modules.values_list('module_id'))
    semestres = Semestre.objects.filter(
        id__in=modules.values_list('semestre_id'))
    niveaux = Niveau.objects.filter(
        id__in=semestres.values_list('niveau_id'))
    filieres = Filiere.objects.filter(id__in=niveaux.values_list('filiere_id'))

    annees = Chapitre.objects.annotate(year=ExtractYear('created_at'))

    # print('annes', annees)

    chapitres = Chapitre.objects.filter(
        created_at__contains=val, deleted=False)

    search_by = "crées pendant l'année \" "+val + " \""

    search_chapitre = request.GET.get('search')
    if search_chapitre:
        chapitres = Chapitre.objects.filter((Q(libelle__icontains=search_chapitre) | Q(
            description__icontains=search_chapitre)) & Q(professeur=professeur.id) & Q(created_at__contains=val) & Q(deleted=False))
        search_by += " qui contiennent \" " + search_chapitre + " \""

    page = request.GET.get('page', 1)
    paginator = Paginator(chapitres, 10)
    try:
        chapitres_page = paginator.page(page)
    except PageNotAnInteger:
        chapitres_page = paginator.page(1)
    except EmptyPage:
        chapitres_page = paginator.page(paginator.num_pages)

    context = {
        "chapitres": chapitres_page,
        "professeur": professeur,
        "filieres": filieres,
        "niveaux": niveaux,
        "element_modules": element_modules,
        "annees": annees,
        "search_by": search_by,
        "new_chapitre": new_chapitre
    }

    return render(request, "cours/chapitres.html", context)


@login_required
def chapitre_details(request, id):
    professeur = Professeur.objects.filter(user_id=request.user.id).first()
    chapitre = Chapitre.objects.filter(id=id).first()
    traitements = Traitement.objects.filter(chapitre_id=id).all()
    documents = Document.objects.filter(chapitre_id=id).all()

    page = request.GET.get('page', 1)
    paginator = Paginator(traitements, 50)
    try:
        traitements_page = paginator.page(page)
    except PageNotAnInteger:
        traitements_page = paginator.page(1)
    except EmptyPage:
        traitements_page = paginator.page(paginator.num_pages)

    context = {
        "chapitre": chapitre,
        "professeur": professeur,
        "traitements": traitements_page,
        "documents": documents,
    }
    return render(request, 'cours/chapitre_details.html', context)


@login_required
def add_chapitre(request):
    professeur = Professeur.objects.filter(user_id=request.user.id).first()
    if request.method == "GET":
        new_chapitre = ChapitreForm(request=request)
    elif request.method == "POST":
        new_chapitre = ChapitreForm(
            request.POST, request.FILES, request=request)
        if new_chapitre.is_valid():
            chapitre = new_chapitre.save(commit=False)
            chapitre.professeur = professeur
            chapitre.save()
            messages.success(request, ('Le chapitre a été ajouté avec succès'))
            return redirect('chapitres_list')
        else:
            messages.error(request, 'Erreur : Le chapitre n\'a pas été ajouté')
            return redirect('add_chapitre')
    return render(request, 'cours/add_chapitre.html', context={'new_chapitre': new_chapitre})


@login_required
def delete_chapitre(request, id):
    chapitre = Chapitre.objects.get(id=id)
    chapitre.deleted = True
    # if chapitre.delete():
    saved = chapitre.save()
    if not saved:
        messages.success(request, ('Le chapitre a été supprimé !'))
    else:
        messages.error(request, 'Erreur : Le chapitre n\'a pas été supprimé')
    return redirect('chapitres_list')


@login_required
def update_chapitre(request, id):
    chapitre = Chapitre.objects.get(id=id)
    if request.method == "GET":
        updated_chapitre = ChapitreForm(instance=chapitre, request=request)
    elif request.method == "POST":
        updated_chapitre = ChapitreForm(
            request.POST, request.FILES, instance=chapitre, request=request)
        if updated_chapitre.is_valid():
            updated_chapitre.save()
            messages.success(
                request, ('Le chapitre a été modifié avec succès'))
            return redirect('chapitres_list')
        else:
            messages.error(
                request, 'Erreur : Le chapitre n\'a pas été modifié')
            return redirect('update_chapitre')
    return render(request, 'cours/update_chapitre.html', context={'updated_chapitre': updated_chapitre})


# Documents Methods-----------
EXTENSIONS_DOC = ['pdf', 'docx', 'ppt', 'txt']


@login_required
def add_document(request, id):
    professeur = Professeur.objects.filter(
        user_id=request.user.id).first()
    chapitre = Chapitre.objects.filter(id=id).first()
    print("")
    if request.method == "GET":
        new_document = DocumentForm(request=request)
    elif request.method == "POST":
        # print('<message>', file=sys.stderr)
        print('post : ', request.POST)

        new_document = DocumentForm(
            request.POST, request.FILES, request=request)

        invalid_extension = 0
        if new_document.is_valid():
            file = request.FILES.get('path')
            filename = file.name
            # for f in files:
            #   filebase, extension = f.name.split('.')
            #   if EXTENSIONS_DOC.__contains__(extension):
            #    ...
            #   else:
            #     invalid_extension += 1
            #     messages.error(
            #     request, 'Erreur : L\'extension n\'est pas autorisée !')
            #     return redirect('add_document')

            # if invalid_extension == 0:
            document = new_document.save(commit=False)
            document.chapitre = chapitre
            if filename.endswith('.docx') or filename.endswith('.doc'):
                document.type = "docx"
            elif filename.endswith('.pdf'):
                document.type = "pdf"
            elif filename.endswith('.txt'):
                document.type = "txt"
            elif filename.endswith('.ppt'):
                document.type = "ppt"
            elif filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png') or filename.endswith('.jfif'):
                document.type = "jpg"
            else:
                document.type = "autre"
            document.save()
            messages.success(
                request, ('Le document a été ajouté avec succes!'))
            return redirect('chapitres_list')
            # else:
            #     messages.error(
            #     request, 'Erreur : Le document que vous avez entrer ne peut pas être acceptée  !')
            #     return redirect('add_document')

        else:
            messages.error(
                request, 'Erreur : Le document que vous avez entrer ne peut pas être acceptée !')
            return redirect('add_document')

    return render(request, 'cours/add_document.html', context={'new_document': new_document})


@login_required
def delete_document(request, id):
    document = Document.objects.get(id=id)
    if document.delete():
        messages.success(request, ('Le document a été supprimé !'))
    else:
        messages.error(request, 'Erreur : Le document n\'a pas été supprimé')
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


@login_required
def update_document(request, id):
    document = Document.objects.get(id=id)
    if request.method == "GET":
        updated_document = DocumentForm(instance=document, request=request)
    elif request.method == "POST":
        updated_document = DocumentForm(
            request.POST, request.FILES, instance=document, request=request)
        if updated_document.is_valid():
            document = updated_document.save(commit=False)
            file = request.FILES.get('path')
            filename = file.name
            if filename.endswith('.docx'):
                document.type = "docx"
            elif filename.endswith('.pdf'):
                document.type = "pdf"
            elif filename.endswith('.txt'):
                document.type = "txt"
            elif filename.endswith('.ppt'):
                document.type = "ppt"
            elif filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png') or filename.endswith('.jfif'):
                document.type = "jpg"
            else:
                document.type = "autre"
            document.save()
            messages.success(
                request, ('Le document a été modifié avec succès'))
            return redirect('chapitres_list')
        else:
            messages.error(
                request, 'Erreur : Le docuement n\'a pas été modifié')
            return redirect('update_document')
    return render(request, 'cours/update_document.html', context={'updated_document': updated_document})


@api_view(['GET'])
def documents_list_api(request, id_chapitre):
    try:
        documents = Document.objects.filter(
            chapitre_id=id_chapitre).defer('id')
        documents_serializer = DocumentSerializerImage(documents, many=True)
        return Response(documents_serializer.data)
    except Document.DoesNotExist:
        return Response([])


@api_view(['GET'])
def get_Document(request, id):
    try:
        Documents = Document.objects.filter(chapitre_id=id).all()
        serializer = DocumentSerializerImage(Documents, many=True)
        return Response(serializer.data)
    except Document.DoesNotExist:
        return Response([])


@login_required
def delete_modele(request, id):
    traitement = Traitement.objects.get(id=id)
    modele = Modele3D.objects.get(id=traitement.modele3D.id)
    if traitement.image is not NULL:
        image = Image.objects.get(id=traitement.image.id)
        image.delete()
    if traitement.delete() & modele.delete():
        messages.success(request, ('Le Modèle 3D a été supprimé !'))
    else:
        messages.error(request, 'Erreur : Le Modèle 3D n\'a pas été supprimé')
    return redirect('#')


@login_required
def delete_image(request, id):
    traitement = Traitement.objects.get(id=id)
    image = Image.objects.get(id=traitement.image.id)
    if image.delete():
        messages.success(request, ('L\'image a été supprimé !'))
    else:
        messages.error(request, 'Erreur : L\'image n\'a pas été supprimé')
    return redirect('#')


@login_required
def delete_Traitement(request, id):
    traitement = Traitement.objects.get(id=id)
    if traitement.delete():
        messages.success(request, ('Le modele AR a été supprimé !'))
    else:
        messages.error(request, 'Erreur : Le modele  n\'a pas été supprimé')
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


EXTENSIONS = ['jpg', 'jpeg', 'png', 'bin', 'gltf', 'glb']


@login_required
def add_traitement(request, id):
    professeur = Professeur.objects.filter(
        user_id=request.user.id).first()
    chapitre = Chapitre.objects.filter(id=id).first()

    Traitements_visibles = Traitement.objects.filter(visibilite=professeur)
    modeles_visibles = Modele3D.objects.filter(
        id__in=[val.id for val in Traitements_visibles])
    if request.method == "GET":
        new_traitement = TraitementForm(request=request)
        new_image = ImageForm()
        new_modele3d = Modele3DForm()
        new_file = FileForm()

    elif request.method == "POST":
        # print('<message>', file=sys.stderr)
        print('post : ', request.POST)

        new_traitement = TraitementForm(
            request.POST, request.FILES, request=request)

        invalid_extension = 0

        if new_traitement.is_valid():
            print('post : valid')

            traitement = new_traitement.save(commit=False)
            traitement.chapitre = chapitre
            print('<traitement>'+traitement.type_traitement, file=sys.stderr)

            new_modele3d = Modele3DForm(request.POST, request.FILES)

            if request.POST.get("modele3D") != '':

                existant_modele3d = Modele3D.objects.get(
                    id=request.POST.get("modele3D"))

                if traitement.type_traitement == "Texte":

                    traitement.image = None
                else:
                    new_image = ImageForm(request.POST, request.FILES)
                    if new_image.is_valid():
                        image = new_image.save(commit=False)
                        if traitement.type_traitement == "Image":
                            image.is_qrcode = False
                        elif traitement.type_traitement == "QR-Code":
                            image.is_qrcode = True

                        image.save()
                        traitement.image = image
                    else:
                        messages.error(
                            request, 'Erreur : L\'image que vous avez entrer ne peut pas être acceptée !')

                traitement.modele3D = existant_modele3d

                traitement.save()
                traitement.visibilite.add(professeur)
                messages.success(request, ('Le modele AR a été ajouté !'))
            elif new_modele3d.is_valid():
                print('post : modele 3d', request.POST.get("modele3D") != '')

                new_modele = new_modele3d.save(commit=False)
                new_modele.path_modele3d = model_location(
                    new_modele3d['titre_modele3d'].value())
                makedirs(new_modele.path_modele3d)

                new_modele.save()

                files = request.FILES.getlist('path_file')

                for f in files:
                    filebase, extension = f.name.rsplit('.', 1)
                    if EXTENSIONS.__contains__(extension):
                        ...
                    else:
                        invalid_extension += 1
                        messages.error(
                            request, 'Erreur : L\'extension n\'est pas autorisée !')

                if invalid_extension == 0:
                    for f in files:
                        obj = File.objects.create(
                            modele3D=new_modele, path_file=f)

                    if traitement.type_traitement == "Texte":
                        str = traitement.label_traitement
                        chunks = str.split(',')
                        mylist = [f"{s}," for s in chunks]
                        print(mylist)
                        data = ','
                        for word in mylist:
                            data += word
                        traitement.label_traitement = data
                        traitement.image = None
                    else:
                        new_image = ImageForm(request.POST, request.FILES)
                        print("_____________________________")
                        print(new_image)
                        if new_image.is_valid():
                            image = new_image.save(commit=False)
                            if traitement.type_traitement == "Image":

                                image.is_qrcode = False
                                image.save()

                            elif traitement.type_traitement == "QR-Code":
                                # path_file ="img/cours/modeles_3d/"+new_modele3d['titre_modele3d'].value()+"/"+f.name

                                files_set = []
                                files = File.objects.filter(
                                    modele3D=new_modele)
                                file_serializer = FileSerializerImage(
                                    files, many=True)
                                for val in file_serializer.data:
                                    files_set.append(val['path_file'])
                                file = None
                                for val in files_set:
                                    ext = val.split('.')[-1]
                                    # print(ext)
                                    if(ext == 'glb'):
                                        file = val
                                    elif(ext == 'gltf'):
                                        file = val

                                path_file = file
                                # img/cours/modeles_3d/
                                qr = qrcode.QRCode(
                                    version=1,
                                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                                    box_size=10,
                                    border=4,
                                )
                                qr.add_data(path_file)
                                qr.make(fit=True)

                                img = qr.make_image(
                                    fill_color="black", back_color="white")
                                # filename = "khadija qr.jpeg"
                                # cv2.imwrite('img/cours/chapitre_images/qr/code_test2_2.png', i)
                                # img.save('img/cours/qr/'+'hhhhhh.png')
                                print(img)
                                image.is_qrcode = True

                                # extension = f.name.split('.')
                                extension = '.png'
                                now = time.time()
                                stamp = datetime.datetime.fromtimestamp(
                                    now).strftime('%Y-%m-%d-%H-%M-%S')
                                img_name = stamp + extension
                                img.save("media/img/cours/qr_images/"+img_name)
                                image.path_image = 'img/cours/qr_images/' + img_name

                                image.save()
                                # canvas.close()
                            # image.save(img)
                            traitement.image = image
                        else:
                            messages.error(
                                request, 'Erreur : L\'image que vous avez entrer ne peut pas être acceptée !')
                    traitement.modele3D = new_modele
                    traitement.save()
                    traitement.visibilite.add(professeur)

                    messages.success(request, ('Le modele AR a été ajouté !'))

            else:
                messages.error(
                    request, 'Erreur : Le modèle ne peut pas être enregistré !')

        else:
            messages.error(
                request, 'Erreur : Le modèle ne peut pas être enregistré !')
        return redirect('chapitre_details', id)

    return render(request, 'cours/add_traitement.html', context={'new_traitement': new_traitement, 'new_modele3d': new_modele3d, 'new_image': new_image, 'new_file': new_file, 'modeles_visibles': modeles_visibles
                                                                 #  , 'trait': trait
                                                                 })


@login_required
def traitement_details(request):
    # if request.is_ajax and request.method == "GET":
    traitement_id = request.GET.get("traitement_id", None)
    professeur = Professeur.objects.filter(
        user_id=request.user.id).first()

    traitement = Traitement.objects.filter(id=traitement_id).first()
    modele3d = Modele3D.objects.filter(id=traitement.modele3D_id).first()
    files = File.objects.filter(modele3D=modele3d).all()
    # fileCount = {"count": files}
    if(traitement.type_traitement != "Texte"):
        image = Image.objects.filter(id=traitement.image_id).first()
        context = {
            "traitement": json.loads(serialize('json', [traitement]))[0],
            "professeur": json.loads(serialize('json', [professeur]))[0],
            "modele3d": json.loads(serialize('json', [modele3d]))[0],
            "files": serialize('json', files),
            "image": json.loads(serialize('json', [image]))[0]
        }
    else:
        context = {
            "traitement": json.loads(serialize('json', [traitement]))[0],
            "professeur": json.loads(serialize('json', [professeur]))[0],
            "modele3d": json.loads(serialize('json', [modele3d]))[0],
            "files": serialize('json', files),
        }
    return JsonResponse(context, status=200)


def file_upload_location(modele3d, filename):

    path_modele3d = modele3d.path_modele3d
    return '%s/%s' % (path_modele3d, filename)


def model_location(modelName):
    now = time.time()
    stamp = datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d-%H-%M-%S')
    return 'img/cours/modeles_3d/%s-%s' % (modelName, str(stamp))


def handle_file_upload(f, new_modele):
    with open(file_upload_location(new_modele, f.name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def makedirs(path):

    try:
        os.makedirs(os.path.join('/media/', path))
    except OSError as e:
        if e.errno == 17:
            pass


@login_required
def update_traitement(request, id):
    professeur = Professeur.objects.filter(
        user_id=request.user.id).first()
    traitement = Traitement.objects.filter(id=id).first()
    q = Traitement.objects.filter(id=id).annotate(Count('id'))
    type_traitement = q[0].type_traitement
    chapitre_id = q[0].chapitre_id
    modele3d = Modele3D.objects.filter(id=traitement.modele3D_id).first()
    files = File.objects.filter(modele3D=modele3d).all()
    if type_traitement != 'Texte':
        image = Image.objects.filter(id=traitement.image_id).first()
    updated_image = None

    if request.method == "GET":
        updated_traitement = TraitementForm(
            instance=traitement, request=request)
        updated_modele3d = Modele3DForm(instance=modele3d, request=request)
        if type_traitement != 'Texte':
            updated_image = ImageForm(instance=image, request=request)

    elif request.method == "POST":
        updated_traitement = TraitementForm(
            request.POST, request.FILES, instance=traitement, request=request)
        updated_modele3d = Modele3DForm(
            request.POST, request.FILES, instance=modele3d, request=request)
        if type_traitement != 'Texte':
            updated_image = ImageForm(
                request.POST, request.FILES, instance=image, request=request)

        if updated_traitement.is_valid():
            visibilite_profs = updated_traitement.cleaned_data.get(
                "visibilite")

            traitement = updated_traitement.save(commit=False)
            traitement.type_traitement = type_traitement
            if updated_modele3d.is_valid():
                updated_modele3d = updated_modele3d.save()

                if traitement.type_traitement != "Texte":
                    if updated_image.is_valid():
                        updated_image = updated_image.save()
                        traitement.image = updated_image
                    else:
                        messages.error(
                            request, 'Erreur : L\'image que vous avez entré ne peut pas être acceptée !')
                traitement.modele3D = updated_modele3d
                traitement.save()

                for prof in Professeur.objects.all():

                    traitement.visibilite.remove(prof)
                traitement.visibilite.add(professeur)
                for prof in visibilite_profs:
                    prof_exist = 0
                    for visible in traitement.visibilite.all():
                        if(prof.pk == visible.pk):
                            prof_exist += 1
                            print('equal')
                        if(prof_exist == 0):
                            print('inexist')
                            traitement.visibilite.add(prof)
                messages.success(request, ('Le modele AR a été modifié !'))
            else:
                messages.error(
                    request, 'Erreur : Le modèle ne peut pas être enregistré !')
        else:
            messages.error(
                request, 'Erreur : Le modèle ne peut pas être enregistré !' + traitement.type_traitement)
        return redirect('chapitre_details', chapitre_id)

    return render(request, 'cours/update_traitement.html', context={'updated_traitement': updated_traitement, 'updated_modele3d': updated_modele3d, 'updated_image': updated_image                                                                    # , 'new_file': new_file
                                                                    , 'updated_files': files
                                                                    #  , 'trait': trait
                                                                    })


# API

@api_view(['GET'])
def chapitres_list_api(request, id_module):
    chapitres = Chapitre.objects.filter(element_module_id=id_module)
    chapitre_serializer = ChapitreSerializer(
        chapitres, many=True)

    return Response(chapitre_serializer.data)


@api_view(['GET'])
def chapitre_details_api(request, id_chapitre):
    chapitre = Chapitre.objects.get(id=id_chapitre)
    chapitre_serializer = ChapitreSerializer(chapitre, many=False)
    return Response(chapitre_serializer.data)


@api_view(['GET'])
def traitements_list_api(request, id_chapitre):

    traitements = Traitement.objects.filter(chapitre_id=id_chapitre)
    traitement_serializer = TraitementSerializerImage(traitements, many=True)

    modele3d = Modele3D.objects.filter(
        id__in=[t.modele3D_id for t in traitements])
    modele3d_serializer = Modele3DSerializerImage(modele3d, many=True)
    image_serializer = []

    files_set = []

    files = File.objects.filter(modele3D=modele3d)
    file_serializer = FileSerializerImage(files, many=True)

    res = []

    for i in range(0, len(traitement_serializer.data)):

        # print(traitements[i].modele3D_id)

        modele3d = Modele3D.objects.get(
            id=traitements[i].modele3D_id)
        modele3d_serializer = Modele3DSerializerImage(modele3d, many=False)

        image = None
        try:
            image = Image.objects.get(id=traitements[i].image_id)
            image_serializer = ImageSerializerImage(image, many=False)
        except Image.DoesNotExist:
            image = None
            image_serializer = None
        # print(image)
        if image != None:
            path_image = image_serializer.data['path_image']
        else:
            path_image = None

        files_set = []
        files = File.objects.filter(modele3D=modele3d)
        file_serializer = FileSerializerImage(files, many=True)
        for val in file_serializer.data:
            files_set.append(val['path_file'])
        file = None
        for val in files_set:
            ext = val.split('.')[-1]
            # print(ext)
            if(ext == 'glb'):
                file = val
            elif(ext == 'gltf'):
                file = val
            # elif(ext == 'png'):
            #     file = val
            # elif(ext == 'jpg'):
            #     file = val

        res.append(
            {'id': traitement_serializer.data[i]['id'],
             'nom': traitement_serializer.data[i]['titre_traitement'],
             #  'path_modele3d': modele3d_serializer.data['path_modele3d'],
             'path_modele3d': file,
             'path_image': path_image
             })

    return Response(res)


@api_view(['GET'])
def traitement_api(request, id):
    traitement = Traitement.objects.filter(id=id).first()

    traitement_serializer = TraitementSerializerImage(traitement, many=False)

    modele3d = Modele3D.objects.filter(
        id=traitement.modele3D_id).first()

    files_set = []
    files = File.objects.filter(modele3D=modele3d)
    file_serializer = FileSerializerImage(files, many=True)
    for val in file_serializer.data:
        files_set.append(val['path_file'])
    file = None
    for val in files_set:
        ext = val.split('.')[-1]
        # print(ext)
        # if(ext == 'png'):
        #     file = val
        # elif(ext == 'jpg'):
        #     file = val

        if(ext == 'glb'):
            file = val
        elif(ext == 'gltf'):
            file = val

    image_serializer = None

    image = Image.objects.filter(id=traitement.image_id).first()
    image_serializer = ImageSerializerImage(image, many=False)
    response = {
        'traitement': traitement_serializer.data['titre_traitement'],
        'file': file,
        'image': image_serializer.data['path_image']
    }
    return Response(response)
