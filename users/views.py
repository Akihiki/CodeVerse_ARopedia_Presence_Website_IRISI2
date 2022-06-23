from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required, user_passes_test

from users.EmailBackEnd import EmailBackEnd


def home(request):
    return render(request, 'users/index.html')


def loginPage(request):
    return render(request, 'users/login.html')


def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get(
            'email'), password=request.POST.get('password'))
        if user != None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            user_type = user.user_type
            if user_type == '1':
                return redirect('admin_home')

            elif user_type == '2':
                return redirect('teacher_home')

            elif user_type == '3':
                return redirect('student_home')
            else:
                messages.error(request, "Invalid Login!")
                return redirect('login')
        else:
            messages.error(request, "Invalid Login Credentials!")
            # return HttpResponseRedirect("/")
            return redirect('login')


def get_user_details(request):
    if request.user != None:
        return HttpResponse("User: "+request.user.email+" User Type: "+request.user.user_type)
    else:
        return HttpResponse("Please Login First")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')
