from django.shortcuts import render, redirect
from django import forms

from users.models import Role, Permission
from users.roleForm import GeeksForm

# UnivIt responsable : ismail errouk
def manageRoles(request):
    roles = Role.objects.all()
    return render(request, 'roles_permissions/manage_Role_template.html', {'roles': roles})

# UnivIt responsable : ismail errouk
def addRole(request):
    context = {}
    context['form'] = GeeksForm()
    return render(request, "roles_permissions/add_Role_template.html", context)

# UnivIt responsable : ismail errouk
def addRoleSave(request):
    global temp
    context = {}
    form = GeeksForm(request.POST or None)
    context['form'] = form
    if request.POST:
        libelle = request.POST['libelle']
        description = request.POST['description']
        if form.is_valid():
            temp = form.cleaned_data.get("Permissions")
        permissions = []
        for t in temp:
            print("hey " + t)
            permissions.append(Permission.objects.get(pk=int(t)))
        role = Role()
        role.libelle = libelle
        role.description = description
        role.save()
        for permission in permissions:
            role.permissions.add(permission)
    return redirect(to='manage_roles')

# UnivIt responsable : ismail errouk
def deleteRole(request, id):
    role = Role.objects.get(id=id)
    role.delete()
    return redirect(to='manage_roles')

# UnivIt responsable : ismail errouk
def editRole(request, id):
    role = Role.objects.get(id=id)
    permissions = role.permissions.all()
    print(permissions.count())
    for permission in permissions:
        print(permission.libelle)

    context = {
        'form': GeeksForm(),
        'role': role,
        'permissions': permissions
    }
    return render(request, "roles_permissions/edit_role_template.html", context)

# UnivIt responsable : ismail errouk
def editRoleSave(request, id):
    global temp
    context = {}
    form = GeeksForm(request.POST or None)
    context['form'] = form
    if request.POST:
        role_lib = request.POST['libelle']
        role_description = request.POST['description']
        if form.is_valid():
            temp = form.cleaned_data.get("Permissions")
        permissions = []
        for t in temp:
            print("hey " + t)
            permissions.append(Permission.objects.get(pk=int(t)))
        role = Role.objects.get(pk=int(id))
        role.libelle = role_lib
        role.description = role_description
        for permission in permissions:
            role.permissions.add(permission)
        role.save()
    return redirect(to='edit_role', id=id)

# UnivIt responsable : ismail errouk
def deleteRolePermission(request, id1, id2):
    role = Role.objects.get(pk=id1)
    permission = Permission.objects.get(pk=id2)
    role.permissions.remove(permission)
    return redirect(to='edit_role', id=id1)
