import json
import os
import csv
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage  # To upload Profile Picture
from django.urls import reverse
import datetime  # To Parse input DateTime into Python Date Time Object
from datetime import date
from django.utils.datastructures import MultiValueDictKeyError
from semestre.models import Groupe
from users.forms import EditStudentForm, AddStudentForm
from users.models import *
from users.roleForm import GroupeListForm
from rest_framework.decorators import api_view
from django.http import JsonResponse
from semestre.models import AnneUniversitaire
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def student_home(request):
    return render(request, "student/student_home_template.html")


def student_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    student = Students.objects.get(admin=user)

    context = {
        "user": user,
        "student": student
    }
    return render(request, 'student/student_profile.html', context)


def student_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('student_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            student = Students.objects.get(admin=customuser.id)
            student.address = address
            student.save()

            messages.success(request, "Profile Updated Successfully")
            return redirect('student_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('student_profile')


# UnivIt responsable : ismail errouk
# def add_student(request, id=0):
#     users = CustomUser.objects.all()
#     if request.method == 'GET':
#         if id == 0:
#             form = AddStudentForm()  # form vide
#         else:
#             student = Students.objects.get(pk=id)
#             form = AddStudentForm(instance=student)  # form remplie par employee
#
#         # return render(request, 'users/etudiants/etudiant_form.html', {'form': form, 'users': users})
#         return render(request, 'admin/add_student_template.html', {'form': form, 'users': users})
# UnivIt responsable : ismail errouk
def add_student(request, id=0):
    admins = Admin.objects.all()
    if request.method == 'GET':
        # form remplie par employee
        # return render(request, 'users/etudiants/etudiant_form.html', {'form': form, 'users': users})
        return render(request, 'student/add_student_template.html', {'admins': admins})


# UnivIt responsable : ismail errouk
# def add_student_save(request):
#     global student
#     form = AddStudentForm(request.POST, request.FILES)
#     if form.is_valid():
#         adresse = form.cleaned_data['adresse']
#         admin = form.cleaned_data['admin']
#         user = form.cleaned_data['user']
#         # print(admin.admin.admin)
#         print(user.username)
#         cne = form.cleaned_data['cne']
#         code_apogee = form.cleaned_data['code_apogee']
#         telephone = form.cleaned_data['telephone']
#         path_photos = form.cleaned_data['path_photos']
#         form.save()
#         student = Students.objects.get(cne=cne)
#
#     return redirect(to='add_student_groups', id=student.id)
# UnivIt responsable : ismail errouk
def add_student_save(request):
    global student
    if request.method == 'POST':
        admin = Admin.objects.get(id=request.POST['select_admin'])

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        user = CustomUser()
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.username = request.POST['first_name'] + \
            '_' + request.POST['last_name']
        user.user_type = 'STUDENT'
        if request.POST['password'] == request.POST['confirm_password']:
            user.set_password(request.POST['password'])
        user.save()
        student = Students()
        student.user = user
        student.admin = admin
        student.cne = request.POST['cne']
        student.adresse = request.POST['adresse']
        # student.profile_pic = request.POST['profile_pic']
        student.profile_pic = handle_uploaded_file(
            request.FILES['profile_pic'])
        student.path_photos = "face_recognition/service_metier/dataset/Etudiant_" + \
            first_name + "_" + last_name + "/"
        student.telephone = request.POST['telephone']
        student.code_apogee = request.POST['code_apogee']
        student.save()
    return redirect(to='add_student_groups', id=student.id)


def handle_uploaded_file(f):
    filebase, extension = f.name.split('.')
    now = time.time()
    stamp = datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d-%H-%M-%S')
    name = str(stamp)+'.'+extension
    path = os.path.join('media/img/etudiant/', name)
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return path

def handle_uploaded_csv_file(f):
    filebase, extension = f.name.split('.')
    # now = time.time()
    # stamp = datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d-%H-%M-%S')
    name = 'etudiants.'+extension
    path = os.path.join('media/files/etudiant/', name)
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return path


@api_view(['GET'])
def getAllStudents(request):
    all_students = Students.objects.all()
    students = []
    for student in all_students:
        groupes = student.groupes.all()
        student_groupes = []
        for groupe in groupes:
            student_groupes.append(
                {'nom groupe': groupe.nom_group, 'niveau': groupe.niveau.nom_niveau})
        students.append({
            'first_name': student.user.first_name,
            'last_name': student.user.last_name,
            'username': student.user.username,
            'email': student.user.email,
            'cne': student.cne,
            'adresse': student.adresse,
            'telephone': student.telephone,
            'code apogee': student.code_apogee,
            'path photos': student.path_photos,
            'groupes': student_groupes
        })
    return JsonResponse(students, safe=False)
    # return JsonResponse(students)


# UnivIt responsable : ismail errouk
def add_student_groups(request, id):
    context = {}
    context['form'] = GroupeListForm()
    context['id'] = id
    return render(request, "student/add_Student_Groupe_template.html", context)


# UnivIt responsable : ismail errouk
def add_student_groups_save(request, id):
    global temp
    context = {}
    form = GroupeListForm(request.POST or None)
    context['form'] = form
    if request.POST:
        if form.is_valid():
            temp = form.cleaned_data.get("Groupes")
        groupes = []
        for t in temp:
            print("hey " + t)
            groupes.append(Groupe.objects.get(pk=int(t)))
        student = Students.objects.get(pk=id)
        for groupe in groupes:
            student.groupes.add(groupe)
            annee = AnneUniversitaire()
            annee.group=groupe
            annee.libelle=request.POST  ['annee_univ']
            annee.etudiant=student
            annee.date = date.today()
            annee.save()
        student.save()

    return redirect(to='manage_student')


# UnivIt responsable : ismail errouk
def manage_student(request):
    students = Students.objects.all()
    all_students_count = Students.objects.all().count()
    page = request.GET.get('page', 1)
    pag = Paginator(students, 8)
    try:
        astudents = pag.page(page)
    except PageNotAnInteger:
        astudents = pag.page(1)
    except EmptyPage:
        astudents = pag.page(pag.num_pages)
    context = {
        "students": astudents,
        "all_students_count": all_students_count
    }
    return render(request, 'student/manage_student_template.html', context)


def add_csv_file_student(request):
    path = handle_uploaded_csv_file(request.FILES['csv_file'])
    # path = os.path.join('media/files/etudiant/', 'users.csv')
    admin = Admin.objects.get(id=1)
    with open(path) as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header
        for row in reader:
            print(row)
            user = CustomUser()
            user.first_name = row[0]
            user.last_name = row[1]
            user.email = row[2]
            user.username = row[0] + \
                            '_' + row[1]
            user.user_type = 'STUDENT'
            user.set_password(row[3])
            user.save()
            student = Students()
            student.user = user
            student.admin = admin
            student.cne = row[4]
            student.adresse = row[5]
            # student.profile_pic = request.POST['profile_pic']
            student.profile_pic = "need to update"
            student.path_photos = "face_recognition/dataset/Etudiant_" + \
                                  row[0] + "_" + row[1] + "/"
            student.telephone = row[6]
            student.code_apogee = row[7]
            student.save()
    return redirect(to='manage_student')


def insert_csv_file_to_database():
    return True

# UnivIt responsable : ismail errouk
def edit_student(request, student_id):
    # Adding Student ID into Session Variable
    request.session['student_id'] = student_id

    student = Students.objects.get(id=student_id)
    print(student.cne)
    form = EditStudentForm()
    # Filling the form with Data from Database
    form.fields['cne'].initial = student.cne
    form.fields['adresse'].initial = student.adresse
    form.fields['path_photos'].initial = student.path_photos
    form.fields['telephone'].initial = student.telephone
    form.fields['code_apogee'].initial = student.code_apogee

    context = {
        "id": student_id,
        "username": student.user.username,
        "student": student,
        "form": form
    }
    return render(request, "student/edit_student_template.html", context)


# UnivIt responsable : ismail errouk
def edit_student_save(request, id):
    # print('------------')
    # student = Students.objects.get(id=id)
    # form = EditStudentForm(request.POST, request.FILES)
    # if form.is_valid():
    #     student.cne = form.cleaned_data['cne']
    #     student.adresse = form.cleaned_data['adresse']
    #     student.path_photos = form.cleaned_data['path_photos']
    #     student.telephone = form.cleaned_data['telephone']
    #     student.code_apogee = form.cleaned_data['code_apogee']
    #     student.save()
    global student
    if request.method == 'POST':

        student = Students.objects.get(id=id)
        user = student.user
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.username = request.POST['first_name'] + \
            '_' + request.POST['last_name']
        user.user_type = 'STUDENT'
        # user.set_password(request.POST['password'])
        user.save()
        student.cne = request.POST['cne']
        student.adresse = request.POST['adresse']
        student.path_photos = request.POST['path_photos']
        student.telephone = request.POST['telephone']
        student.code_apogee = request.POST['code_apogee']
        try:
            filepath = request.FILES['profile_pic']
            student.profile_pic = handle_uploaded_file(
                request.FILES['profile_pic'])
        except MultiValueDictKeyError:
            filepath = False

        student.save()
    return redirect(to='manage_student')


# UnivIt responsable : ismail errouk
def delete_student_groupe(request, id1, id2):
    student = Students.objects.get(id=id1)
    group = Groupe.objects.get(id=id2)
    student.groupes.remove(group)
    return redirect(to='manage_student')


# UnivIt responsable : ismail errouk
def edit_groupe_add_save(request, id):
    global temp
    if request.method == "POST":
        form = GroupeListForm(request.POST or None)
        if form.is_valid():
            temp = form.cleaned_data.get("Groupes")
        groupes = []
        for t in temp:
            groupes.append(Groupe.objects.get(pk=int(t)))
        student = Students.objects.get(pk=int(id))
        for groupe in groupes:
            student.groupes.add(groupe)
        student.save()
    return redirect(to='manage_student')


# UnivIt responsable : ismail errouk
def edit_groupe_groupes(request, id):
    student = Students.objects.get(id=id)
    groupes = student.groupes.all()
    form = GroupeListForm()
    context = {
        "form": form,
        "student": student,
        "groupes": groupes,
        "id": id
    }
    return render(request, "student/edit_student_groupe_template.html", context)


# UnivIt responsable : ismail errouk
def delete_student(request, student_id):
    student = Students.objects.get(id=student_id)
    try:
        student.delete()
        messages.success(request, "Student Deleted Successfully.")
        return redirect('manage_student')
    except:
        messages.error(request, "Failed to Delete Student.")
        return redirect('manage_student')
