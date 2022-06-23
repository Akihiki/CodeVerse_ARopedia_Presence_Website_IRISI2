from django.urls import path,include


urlpatterns = [
    path('niveau/', include('semestre.urls.niveau')),
    path('semestre/', include('semestre.urls.semestre')),
    path('groupe/', include('semestre.urls.groupe')),        
] 


