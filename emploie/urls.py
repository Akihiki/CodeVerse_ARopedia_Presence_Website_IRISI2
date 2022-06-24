
""" EQUIPE : CODEVERSE
    @author :   + FIROUD REDA et OUSSAHI SALMA
                + KANNOUFA FATIMA EZZAHRA
                + MAROUNI Hicham
"""

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from .api.views import *


urlpatterns = [
    
    # espace admin FIROUD REDA et OUSSAHI SALMA
    path('emploie-admin/', EmploieAdmin, name='emploiAdmin'),
    path('AddPlanning/', AddPlanning, name='AddPlanning'),
    path('AddTypeSalle/', AddTypeSalle, name='AddTypeSalle'),
    path('AddSalle/', AddSalle, name='AddSalle'),
    path('GetGroupes/', GetGroupes, name='GetGroupes'),
    path('GetNiveaux/', GetNiveaux, name='GetNiveaux'),
    path('SendGroupes/', SendGroupes, name='SendGroupes'),
    path('all/', all,name='all'),  
    path('edit/<int:id>', edit),
    path('editTypeSalle/<int:id>', editTypeSalle),    
    path('editSalle/<int:id>', editSalle),    
    path('update/<int:id>', update),  
    path('updateTypeSalle/<int:id>', updateTypeSalle),  
    path('updateSalle/<int:id>', updateSalle),  
    path('delete/<int:id>',destroy, name='destroy'),  
    path('destroyTypeSalle/<int:id>',destroyTypeSalle, name='destroyTypeSalle'),  
    path('destroySalle/<int:id>',destroySalle, name='destroySalle'),  

    
    
    # ecpace prof : KANNOUFA Fatima ezzahra
    path('emploi-prof/', EmploieProf, name='emploiProfesseur'),
    path('liste-presence/<slug:slug>/<int:idSeance>/', ListePresence, name='ListePresence'),
    path('modifier-presence/<int:idSeance>/<int:idEtudiant>/', ModifierPresence, name='ModifierPresence'),
 
    
    # API FIROUD REDA et OUSSAHI SALMA
    path('api/prof/<int:idProf>/seances/', getSeances),
    path('api/get-photo/<path:path_image>/', getPhoto, name="getPhoto"),
    path('api/modifier-presence/<int:idSeance>/<int:idEtudiant>/', modifierPresenceAPI),
    
    # espace etudiant mobile api MAROUNI Hicham
    path('api/etudiant/<int:etudiant_id>/absence', getetudiantpresence),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
