from django.urls import path,include
from semestre.views import niveau 

urlpatterns = [
    path('', niveau.niveau_form,name='niveau_insert'), 
    path('<int:id>/', niveau.niveau_form,name='niveau_update'), 
    path('delete/<int:id>/',niveau.niveau_delete,name='niveau_delete'),
     path('details/<int:id>/',niveau.niveauDelails,name='niveau_details'),
    path('list/',niveau.niveau_list,name='niveau_list') 
]