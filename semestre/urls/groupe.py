from django.urls import path,include
from semestre.views import groupe

urlpatterns = [
    path('', groupe.ajouterGroupe,name='groupe_insert'),
    path('details/<int:id>/', groupe.groupeDetails,name='groupe_details'),  
    path('<int:id>/', groupe.ajouterGroupe,name='groupe_update'), 
    path('delete/<int:id>/',groupe.supprimerGroupe,name='groupe_delete'),
    path('list/',groupe.groupeListe,name='groupe_list') 
]