from django.shortcuts import render, redirect
from django.contrib import messages
from users.models import *


def teacher_home(request):
    return render(request, "teacher/teacher_home_template.html")


# WE don't need csrf_token when using Ajax
# @csrf_exempt
# def get_students(request):
   

def teacher_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    teacher = Professeur.objects.get(admin=user)

    context={
        "user": user,
        "teacher": teacher
    }
    return render(request, 'teacher/teacher_profile.html', context)


def teacher_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('teacher_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        speciality = request.POST.get('speciality')
    
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            teacher = Professeur.objects.get(admin=customuser.id)
            teacher.speciality = speciality
            teacher.save()

            messages.success(request, "Profile Updated Successfully")
            return redirect('teacher_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('teacher_profile')






