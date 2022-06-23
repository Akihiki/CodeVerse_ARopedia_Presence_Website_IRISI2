from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage  # To upload Profile Picture
from django.urls import reverse
import datetime  # To Parse input DateTime into Python Date Time Object

from users.models import *
from users.permissionForm import AddPermissionForm, EditPermissionForm

# UnivIt responsable : ismail errouk
def addPermission(request):
    form = AddPermissionForm()
    return render(request, 'roles_permissions/add_Permission_template.html', {'form': form})

# UnivIt responsable : ismail errouk
def addPermissionSave(request):
    form = AddPermissionForm(request.POST, request.FILES)
    if form.is_valid():
        libelle = form.cleaned_data['libelle']
        description = form.cleaned_data['description']
        form.save()

    return redirect(to='manage_permissions')

# UnivIt responsable : ismail errouk
def editPermission(request, id):
    form = EditPermissionForm()
    permission = Permission.objects.get(id=id)
    form.fields['libelle'].initial = permission.libelle
    form.fields['description'].initial = permission.description

    context = {
        "id": id,
        "form": form
    }
    return render(request, "roles_permissions/edit_permission_template.html", context)

# UnivIt responsable : ismail errouk
def editPermissionSave(request, id):
    form = EditPermissionForm(request.POST, request.FILES)
    permission = Permission.objects.get(id=id)
    if form.is_valid():
        permission.libelle = form.cleaned_data['libelle']
        permission.description = form.cleaned_data['description']
        permission.save()
    return redirect(to='manage_permissions')

# UnivIt responsable : ismail errouk
def deletePermission(request, id):
    permission = Permission.objects.get(id=id)
    permission.delete()
    return redirect(to='manage_permissions')


# UnivIt responsable : ismail errouk
def managePermission(request):
    permissions = Permission.objects.all()
    return render(request, 'roles_permissions/manage_Permission_template.html', {'permissions': permissions})
