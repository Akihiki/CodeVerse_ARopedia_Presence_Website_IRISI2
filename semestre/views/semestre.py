from django.shortcuts import render, redirect 
from semestre.forms.semestre import SemestreForm
from semestre.models import Semestre 

def ajouterSemestre(request , id=0):
    if request.method == "GET":   
        if id == 0 :
            form= SemestreForm()
        else:
            semestre = Semestre.objects.get(pk=id)
            form = SemestreForm(instance=semestre)
        return render(request, "semestre/semestre/semestre_form.html", {'form': form})
    else:
        if id == 0:    
            form = SemestreForm(request.POST)
        else:
            semestre = Semestre.objects.get(pk=id)
            form = SemestreForm(request.POST,instance= semestre)
        if form.is_valid():
            semestre = form.save()
            return redirect('/semestre/semestre/list')



def semestreListe(request):
    context = {'semestre_list': Semestre.objects.all()}
    return render(request, "semestre/semestre/semestre_liste.html", context)

def semestreDetails(request , id):
    semestre = Semestre.objects.get(pk=id)
    form = SemestreForm(instance= semestre)
    form.fields["niveau"].disabled = True
    form.fields["libelle_semestre"].disabled = True
    return render(request, "semestre/semestre/semestre_details.html", {'form': form})


def supprimerSemestre(requst , id):
    semestre = Semestre.objects.get(pk=id)
    semestre.delete()
    return redirect('/semestre/semestre/list')