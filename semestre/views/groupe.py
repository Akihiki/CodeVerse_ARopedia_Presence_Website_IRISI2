from django.shortcuts import render, redirect 
from semestre.forms.groupe import GroupeForm
from semestre.models import Groupe 

def ajouterGroupe(request , id=0):
    if request.method == "GET":   
        if id == 0 :
            form= GroupeForm()
        else:
            groupe = Groupe.objects.get(pk=id)
            form = GroupeForm(instance=groupe)
        return render(request, "semestre/groupe/groupe_form.html", {'form': form})
    else:
        if id == 0:    
            form = GroupeForm(request.POST)
        else:
            groupe = Groupe.objects.get(pk=id)
            form = GroupeForm(request.POST,instance= groupe)
        if form.is_valid():
            groupe = form.save()
            return redirect('/semestre/groupe/list')



def groupeListe(request):
    context = {'groupe_list': Groupe.objects.all()}
    return render(request, "semestre/groupe/groupe_liste.html", context)

def groupeDetails(request , id):
    groupe = Groupe.objects.get(pk=id)
    form = GroupeForm(instance= groupe)
    form.fields["nom_group"].disabled = True
    form.fields["niveau"].disabled = True
    return render(request, "semestre/groupe/groupe_details.html", {'form': form})


def supprimerGroupe(requst , id):
    groupe = Groupe.objects.get(pk=id)
    groupe.delete()
    return redirect('/semestre/groupe/list')