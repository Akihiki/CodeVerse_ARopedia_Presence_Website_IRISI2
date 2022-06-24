
""" RESPONSABLE : CODEVERSE
    @authors    + Espace admin : FIROUD Reda & OUSSAHI Salma
                + Espace professeur : KANNOUFA Fatima Ezzahra
                + Espace etudiant:MAROUNI Hicham
"""

from django.shortcuts import render
from emploie.forms import PlanningForm, SalleForm, TypeSalleForm
from semestre.models import Semestre, Groupe, Niveau
from filiere.models import Filiere
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from slugify import slugify
from emploie.models import Planning, Presence, Seance, TypeSalle, Salle


###   ESPACE ADMIN  ###

#   permet a l'admin de créer les emploies des profs    #
selectefilliere: Filiere
selecteniveau: Niveau
selectegroupe: Groupe

#   CRUD SCEANCE    # FIROUD Reda & OUSSAHI Salma
def EmploieAdmin(request):
    fillieres = Filiere.objects.all()
    semestres = Semestre.objects.all()
    return render(request, 'emploie/espace_admin/pages/emploie_calendar.admin.html', {"filliers": fillieres})
def AddPlanning (request):
    if request.method == "POST":  
        form = PlanningForm(request.POST) 
        if form.is_valid():  
            try:  
                plan=form.save() 
                return redirect('')  
            except: 
                pass  
    else:  
        form = PlanningForm()
    return render(request,'emploie/espace_admin/pages/emploie_calendar.addSchedule.html',{"form":form})

def all(request):  
    plannings = Planning.objects.all()
    return render(request, 'emploie/espace_admin/pages/emploie_calendar.all.html', {"plannings": plannings})

def edit(request, id):  
    plannings = Planning.objects.get(id=id) 
    return render(request, 'emploie/espace_admin/pages/emploie_calendar.edit.html', {'plannings': plannings}) 

def update(request, id):  
    plannings = Planning.objects.get(id=id)  
    form = PlanningForm(request.POST, instance = plannings)
    if form.is_valid():  
        form.save()  
        return redirect("emploie/all")  
    return render(request, 'emploie/espace_admin/pages/emploie_calendar.edit.html', {'plannings': plannings})  

def destroy(request, id):  
    planning = Planning.objects.get(id=id)  
    planning.delete()  
    return redirect("/emploie/all")

#   CRUD TYPESALLE    #FIROUD Reda & OUSSAHI Salma
def AddTypeSalle(request):  
    typesalles = TypeSalle.objects.all()
    if request.method == "POST":  
        form = TypeSalleForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('')  
            except:  
                pass  
    else:  
        form = TypeSalleForm()  
    return render(request,'emploie/espace_admin/pages/emploie_calendar.addTypeSalle.html',{'form':form,"typesalles": typesalles})  

def destroyTypeSalle(request, id):  
    typesalle = TypeSalle.objects.get(id=id)  
    typesalle.delete()  
    return redirect("../AddTypeSalle")

def editTypeSalle(request, id):  
    typesalle = TypeSalle.objects.get(id=id)  
    return render(request,'emploie/espace_admin/pages/emploie_calendar.editTypeSalle.html', {'typesalle':typesalle})  

def updateTypeSalle(request, id):  
    typesalle = TypeSalle.objects.get(id=id)  
    form = TypeSalleForm(request.POST, instance = typesalle)  
    if form.is_valid():  
        form.save()  
        return redirect("../AddTypeSalle")  
    return render(request, 'emploie/espace_admin/pages/emploie_calendar.editTypeSalle.html', {'typesalle': typesalle})

#   CRUD SALLE    ## FIROUD Reda & OUSSAHI Salma

def AddSalle(request): 
    salles = Salle.objects.all() 
    if request.method == "POST":  
        form = SalleForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('')  
            except:  
                pass  
    else:  
        form = SalleForm()  
    return render(request,'emploie/espace_admin/pages/emploie_calendar.addSalle.html',{'form':form,"salles":salles})  

def destroySalle(request, id):  
    salle = Salle.objects.get(id=id)  
    salle.delete()  
    return redirect("../AddSalle")

def editSalle(request, id):  
    salle = Salle.objects.get(id=id)  
    return render(request,'emploie/espace_admin/pages/emploie_calendar.editSalle.html', {'salle':salle})  

def updateSalle(request, id):  
    salle = Salle.objects.get(id=id)  
    form = SalleForm(request.POST, instance = salle)  
    if form.is_valid():  
        form.save()  
        return redirect("../AddSalle")  
    return render(request, 'emploie/espace_admin/pages/emploie_calendar.editSalle.html', {'salle': salle})


def GetNiveaux(request):
    if request.method == 'POST':
        global selectefilliere
        selectefilliere = Filiere.objects.filter(nom_filiere__exact=request.POST['filiereselection']).first()
        niveaux = Niveau.objects.filter(filiere_id__exact=selectefilliere.id).all()
        return render(request, 'emploie/espace_admin/pages/emploie_calendar.admin.html',
                      {"fillier": selectefilliere, "niveaux": niveaux})


def GetGroupes(request):
    if request.method == 'POST':
        global selecteniveau
        selecteniveau = Niveau.objects.filter(id=request.POST['niveauselection']).first()
        groupes = Groupe.objects.filter(niveau_id=selecteniveau.id).all()
        return render(request, 'emploie/espace_admin/pages/emploie_calendar.admin.html',
                      {"fillier": selectefilliere, "niveau": selecteniveau, "groupes": groupes})


def SendGroupes(request):
    if request.method == 'POST':
        global selectegroupe
        selectegroupe = Groupe.objects.filter(id=request.POST['groupeselection']).first()
        plannings = Planning.objects.filter(groupe=selectegroupe)

        return render(request, 'emploie/espace_admin/pages/emploie_calendar.admin.html',
                      {"fillier": selectefilliere, "niveau": selecteniveau, "groupe": selectegroupe,"plannings":plannings})
        



###   ESPACE PROF  #### KANNOUFA FATIMA EZZAHRAE

#   permet d'afficher l'emploi du professeur connécté dans un calendrier    #
@login_required
def EmploieProf(request):
    return render(request, "emploie/espace_prof/pages/emploie_calendar.prof.html")


#   permet de lister les étudiants avec leur présence pour une séance donnée   #
@login_required
def ListePresence(request, slug, idSeance):
    
    seance = Seance.objects.get(pk = idSeance)
    presences = Presence.objects.filter(seance_id = idSeance)
    
    context = {
        "seance" : seance,
        "presences" : presences,
    }
    return render(request, "emploie/espace_prof/pages/liste_presence.prof.html", context)


#   modifier la présence d'un étudiant   #
@login_required
def ModifierPresence(request, idSeance, idEtudiant):
    seance = Seance.objects.get(pk = idSeance)
    slug = slugify(seance.planning.libelle + '-' + str(seance.date))
    
    presence = Presence.objects.get(etudiant_id = idEtudiant, seance_id = idSeance)
    presence.is_present = not presence.is_present
    presence.save()
    
    return redirect('ListePresence', slug=slug, idSeance=idSeance)

###   ESPACE etudiant mobile #MAROUNI Hicham
# retourner la liste de presence
@api_view(['GET'])
def getetudiantpresence(request, etudiant_id):
    #   chercher la liste des persences

    plannings1 = Presence.objects.filter(etudiant_id=etudiant_id)
    #plannings8 = Presence.objects.filter(plannings1)
    seances_etudiant = []
    #   chercher pour chaque presence est qu'il etait present ou non
    for planning in plannings1:
        seances = Presence.objects.filter(
            etudiant_id=etudiant_id, is_present=0)
        seances_etudiant += seances

    serializer1 = PresenceSerializer(seances_etudiant, many=True)

    return Response(serializer1.data)

