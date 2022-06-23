from django.shortcuts import render

# Create your views here.
# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from dashboard.forms import FiliereForm

from dashboard.models import Filiere


# return la page principale
@login_required(login_url="/login/")
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
    context['data'] = data
    html_template = loader.get_template('filieres/filiere.html')
    return HttpResponse(html_template.render(context, request))

# supprission d'une filiere
@login_required(login_url="/login/")
def filiere_delete(request,id):
    filiere = Filiere.objects.get(id=id)
    if filiere.logo:
        if os.path.isfile(filiere.logo.path):
           os.remove(filiere.logo.path)
    filiere.delete()
    return HttpResponseRedirect('/dashboard/filiere')

# rechereche par nom d'une ou des filieres
@login_required(login_url="/login/")
def filiere_search(request):
    context = {}
    if request.method == "POST":
        term = request.POST['text']
        context['segment'] = 'filiere'
        data = Filiere.objects.all()
        context['data'] = data.filter(nom_filiere__icontains = term)
        html_template = loader.get_template('filieres/filiere.html')
        return HttpResponse(html_template.render(context, request))
    html_template = loader.get_template('filieres/page-404.html')
    return HttpResponse(html_template.render(context, request))

# creation d'une nouvelle filiere
@login_required(login_url="/login/")
def filiere_create(request):
    context = {}
    if request.method == "POST":
        form = FiliereForm(request.POST,request.FILES)
        if form.is_valid():
            nom_filiere = form.cleaned_data['nom_filiere']
            logo = form.cleaned_data['logo']
            if not logo :
                data = Filiere(nom_filiere=nom_filiere)
                data.save()
            else:
                data = Filiere(nom_filiere=nom_filiere,logo=logo)
                data.save()
        return HttpResponseRedirect('/dashboard/filiere')
    html_template = loader.get_template('filieres/page-404.html')
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
            if filiere.nom_filiere != nom_filiere:
                filiere.nom_filiere = nom_filiere
            logo = form.cleaned_data['logo']
            if logo :
                if filiere.logo and len(filiere.logo) > 0:
                    os.remove(filiere.logo.path)
                filiere.logo = logo
            filiere.save()
        return HttpResponseRedirect('/dashboard/filiere')
    html_template = loader.get_template('filieres/page-404.html')
    return HttpResponse(html_template.render(context, request))  


# @login_required(login_url="/login/")
# def pages(request):
#     context = {}
#     # All resource paths end in .html.
#     # Pick out the html file name from the url. And load that template.
#     try:

#         load_template = request.path.split('/')[-1]

#         if load_template == 'admin':
#             return HttpResponseRedirect(reverse('admin:index'))
#         context['segment'] = "load_template"
        
#         html_template = loader.get_template('filieres/' + load_template)
#         return HttpResponse(html_template.render(context, request))

#     except template.TemplateDoesNotExist:

#         html_template = loader.get_template('filieres/page-404.html')
#         return HttpResponse(html_template.render(context, request))

#     except:
#         html_template = loader.get_template('filieres/page-500.html')
#         return HttpResponse(html_template.render(context, request))
