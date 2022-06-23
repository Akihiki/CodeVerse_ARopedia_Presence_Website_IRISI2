from django.urls import path, re_path
from filiere import views

urlpatterns = [

    # gestion des Fillieres
    path('', views.index, name='home'),
    path('filiere/', views.filiere, name='filiere'),
    path('filiere/liste/<int:id>', views.filiere_liste, name='filiere_liste'),
    path('filiere/delete/<int:id>', views.filiere_delete, name='filiere_delete'),
    path('filiere/search', views.filiere_search, name='filiere_search'),
    path('filiere/create', views.filiere_create, name='filiere_create'),
    path('filiere/edit/<int:id>', views.filiere_edit, name='filiere_edit'),

    # gestion des Etablissements
    path('etablissement/', views.etablissement, name='etablissement'),
    path('etablissement/liste', views.etablissement_liste, name='etablissement_liste'),
    path('etablissement/delete/<int:id>', views.etablissement_delete, name='etablissement_delete'),
    path('etablissement/search', views.etablissement_search, name='etablissement_search'),
    path('etablissement/create', views.etablissement_create, name='etablissement_create'),
    path('etablissement/edit/<int:id>', views.etablissement_edit, name='etablissement_edit'),
    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),

]