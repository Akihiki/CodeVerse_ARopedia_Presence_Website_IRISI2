from django.urls import path,include
from semestre.views import semestre 

urlpatterns = [
    path('', semestre.ajouterSemestre,name='semestre_insert'),
    path('details/<int:id>/', semestre.semestreDetails,name='semestre_details'),  
    path('<int:id>/', semestre.ajouterSemestre,name='semestre_update'), 
    path('delete/<int:id>/',semestre.supprimerSemestre,name='semestre_delete'),
    path('list/',semestre.semestreListe,name='semestre_list') 
]