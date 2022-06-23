import email
from re import T
from django.shortcuts import render

import os
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
# from django.urls import reverse
from filiere.forms import FiliereForm
from filiere.forms import EtablissementForm

from rest_framework.response import Response
from rest_framework.decorators import api_view

from filiere.models import Filiere
from filiere.models import Etablissement

from .serializers import FiliereSerializer
from .serializers import EtablissementSerializer

######################################################
# gestion des Fillieres
######################################################

#Filiere rest api pour l'envoie de liste des filieres existes
@api_view(['GET'])
def filiere_liste(request,id):
    try:
        etab = Etablissement.objects.get(id=id)
        filieres = Filiere.objects.filter(etablissement__nom=etab.nom)
        serializer = FiliereSerializer(filieres,many=True)
        return Response(serializer.data)
    except Etablissement.DoesNotExist:
        return Response([])

# return la page principale
def index(request):
    context = {'segment': 'index'}
    filieres = Filiere.objects.all()
    context = {'filieres': filieres }
    html_template = loader.get_template('filieres/index.html')
    return HttpResponse(html_template.render(context, request))

# affichage du page de gestion des filieres
@login_required(login_url="/login/")
def filiere(request):
    context = {'segment': 'filiere'}
    data = Filiere.objects.all()
    data2 = Etablissement.objects.all()
    context['data'] = data
    context['data2'] = data2
    html_template = loader.get_template('filiere/filiere.html')
    return HttpResponse(html_template.render(context, request))

# supprission d'une filiere
@login_required(login_url="/login/")
def filiere_delete(request,id):
    filiere = Filiere.objects.get(id=id)
    if filiere.logo:
        if os.path.isfile(filiere.logo.path):
           os.remove(filiere.logo.path)
    filiere.delete()
    return HttpResponseRedirect('/filiere_etab/filiere')

# rechereche par nom d'une ou des filieres
@login_required(login_url="/login/")
def filiere_search(request):
    context = {}
    if request.method == "POST":
        term = request.POST['text']
        context['segment'] = 'filiere'
        data = Filiere.objects.all()
        context['data'] = data.filter(nom_filiere__icontains = term)
        html_template = loader.get_template('filiere/filiere.html')
        return HttpResponse(html_template.render(context, request))
    html_template = loader.get_template('filiere/page-404.html')
    return HttpResponse(html_template.render(context, request))

# creation d'une nouvelle filiere
# @login_required(login_url="/login/")
def filiere_create(request):
    context = {}
    if request.method == "POST":
        form = FiliereForm(request.POST,request.FILES)
        if form.is_valid():
            nom_filiere = form.cleaned_data['nom_filiere']
            id = form.cleaned_data['etablissement']
            etab = Etablissement.objects.get(id=id)
            logo = form.cleaned_data['logo']
            if not logo :
                data = Filiere(nom_filiere=nom_filiere,etablissement=etab)
                data.save()
            else:
                data = Filiere(nom_filiere=nom_filiere,etablissement=etab,logo=logo)
                data.save()
        return HttpResponseRedirect('/filiere_etab/filiere')
    html_template = loader.get_template('filiere/page-404.html')
    return HttpResponse(html_template.render(context, request))
    
# modification d'une filiere
@login_required(login_url="/login/")
def filiere_edit(request,id):
    context = {}
    if request.method == "POST":
        form = FiliereForm(request.POST,request.FILES)
        if form.is_valid():
            filiere = Filiere.objects.get(id= id)
            nom_filiere = form.cleaned_data['nom_filiere']
            id = form.cleaned_data['etablissement']
            if filiere.nom_filiere != nom_filiere:
                filiere.nom_filiere = nom_filiere
            if filiere.etablissement.id != id:
                etab = Etablissement.objects.get(id=id)
                filiere.etablissement = etab
            logo = form.cleaned_data['logo']
            if logo :
                if filiere.logo and len(filiere.logo) > 0:
                    os.remove(filiere.logo.path)
                filiere.logo = logo
            filiere.save()
        return HttpResponseRedirect('/filiere_etab/filiere')
    html_template = loader.get_template('filiere/page-404.html')
    return HttpResponse(html_template.render(context, request))  
    
######################################################
# gestion des Etablissements
######################################################

#Filiere rest api pour l'envoie de liste des filieres existes
@api_view(['GET'])
def etablissement_liste(request):
    try:
        etablissements = Etablissement.objects.all()
        serializer = EtablissementSerializer(etablissements,many=True)
        return Response(serializer.data)
    except Etablissement.DoesNotExist:
        return Response([])

# affichage du page de gestion des etablissements
@login_required(login_url="/login/")
def etablissement(request):
    context = {'segment': 'etablissement'}
    data = Etablissement.objects.all()
    context['data'] = data
    html_template = loader.get_template('filiere/etablissement.html')
    return HttpResponse(html_template.render(context, request))

# supprission d'un etablissement
@login_required(login_url="/login/")
def etablissement_delete(request,id):
    etablissement = Etablissement.objects.get(id=id)
    if etablissement.logo:
        if os.path.isfile(etablissement.logo.path):
           os.remove(etablissement.logo.path)
    etablissement.delete()
    return HttpResponseRedirect('/filiere_etab/etablissement')

# rechereche par nom d'une ou des etablissements
@login_required(login_url="/login/")
def etablissement_search(request):
    context = {}
    if request.method == "POST":
        term = request.POST['text']
        context['segment'] = 'etablissement'
        data = Etablissement.objects.all()
        context['data'] = data.filter(nom__icontains = term)
        html_template = loader.get_template('filiere/etablissement.html')
        return HttpResponse(html_template.render(context, request))
    html_template = loader.get_template('filiere/page-404.html')
    return HttpResponse(html_template.render(context, request))

# creation d'une nouvelle etablissement
@login_required(login_url="/login/")
def etablissement_create(request):
    context = {}
    if request.method == "POST":
        form = EtablissementForm(request.POST,request.FILES)
        if form.is_valid():
            nom = form.cleaned_data['nom']
            adresse = form.cleaned_data['adresse']
            telephone = form.cleaned_data['telephone']
            logo = form.cleaned_data['logo']
            niveau=form.cleaned_data['niveau']
            website=form.cleaned_data['website']
            email=form.cleaned_data['email']
            if not logo :
                data = Etablissement(nom=nom,adresse=adresse,telephone=telephone,niveau=niveau,website=website,email=email)
                data.save()
            else:
                data = Etablissement(nom=nom,adresse=adresse,telephone=telephone,logo=logo,niveau=niveau,website=website,email=email)
                data.save()
        return HttpResponseRedirect('/filiere_etab/etablissement')
    html_template = loader.get_template('filiere/page-404.html')
    return HttpResponse(html_template.render(context, request))
    
# modification d'une etablissement
@login_required(login_url="/login/")
def etablissement_edit(request,id):
    context = {}
    if request.method == "POST":
        form = EtablissementForm(request.POST,request.FILES)
        if form.is_valid():
            etablissement = Etablissement.objects.get(id= id)
            nom = form.cleaned_data['nom']
            adresse = form.cleaned_data['adresse']
            telephone = form.cleaned_data['telephone']
            niveau=form.cleaned_data['niveau']
            website=form.cleaned_data['website']
            email=form.cleaned_data['email']
            if etablissement.nom != nom:
                etablissement.nom = nom
            if etablissement.adresse != adresse:
                etablissement.adresse = adresse
            if etablissement.telephone != telephone:
                etablissement.telephone = telephone
            if etablissement.niveau != niveau:
                etablissement.niveau = niveau
            if etablissement.website != website:
                etablissement.website = website
            if etablissement.email != email:
                etablissement.email = email
            logo = form.cleaned_data['logo']
            if logo :
                if etablissement.logo and len(etablissement.logo) > 0:
                    os.remove(etablissement.logo.path)
                etablissement.logo = logo
            etablissement.save()
        return HttpResponseRedirect('/filiere_etab/etablissement')
    html_template = loader.get_template('filiere/page-404.html')
    return HttpResponse(html_template.render(context, request))  
    
