# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from dashboard import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('filiere/', views.filiere, name='filiere'),
    path('filiere/delete/<int:id>', views.filiere_delete, name='filiere_delete'),
    path('filiere/search', views.filiere_search, name='filiere_search'),
    path('filiere/create', views.filiere_create, name='filiere_create'),
    path('filiere/edit/<int:id>', views.filiere_edit, name='filiere_edit'),

    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),

]
