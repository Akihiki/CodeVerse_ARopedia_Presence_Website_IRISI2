
""" EQUIPE : CodeVerse et ARopedia
    @authors :  + KANNOUFA F. EZZAHRA
                + FIROUD REDA
                + OUSSAHI SALMA
                + MOUZAFIR ABDELHADI
"""

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from .api.views import *

urlpatterns = [
    # machine learning : learning par web 
    path('training/<str:filiere>/<str:niveau>/<str:groupe>/', training , name ='training'),
    path('testerModel/', TesterModel , name ='testerModel'),
    path('testRegisterBD/', testRegisterBD , name ='testRegisterBD'),
    
    # gest_presence : admin dashbord
    path('gestion-presence-modele/', EntrainementAdminDash , name ='EntrainementAdminDash'),
    path('filieres-json/', get_json_filiere_data, name="jsonFilieres"),
    path('niveaux-json/<str:filiere>/', get_json_niveau_data, name="jsonNiveaux"),
    path('groupes-json/<str:niveau>/', get_json_group_data, name="jsonGroupes"),
    
    # rest framework FIROUD Reda & OUSSAHI Salma
    path('mobile/salles/', getSalles, name='salles_list'),
    path('mobile/salles', getSalles, name='salles_list'),
    path('mobile/filieres', filiere_liste, name='filiere_liste'),
    path('mobile/niveau/<str:nom_filiere>', Niveau_liste, name='niveau_liste'),
    path('mobile/salle', RegisterFromPhone, name='RegisterFromPhone'),
    path('mobile/niveau_Choisi', post_niveau, name='post_niveau'),
    
    
    path('api/get-photo-from-backup/<str:filiere>/<str:niveau>/<str:groupe>/<int:idSeance>/<int:idEtudiant>/', getPhotoFromBackup, name="getPhotoFromBackup"),
    
    path('api/presence-test/', presenceTest, name="presenceTest"),

    path('api/presence-test-bd/', testPresenceBD, name="testPresenceBD"),

    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



