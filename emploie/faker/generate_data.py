
""" EQUIPE : CodeVerse
    @author : KANNOUFA FATIMA EZZAHRA
"""

from faker import Faker
from datetime import date
from emploie.models import Planning, Presence, Seance, TypeSalle, Salle
from filiere.models import Etablissement, Filiere
from semestre.models import AnneUniversitaire, Groupe, Niveau, Semestre
from module.models import ElementModule, Module
from users.models import Admin, CustomUser, Students, Professeur
import datetime

  
  
#   Générer des données alétoire à l'aide de faker
#   Tables remplies : Salle, TypeSalle, Etablissement, Filiere, Niveau, Groupe, Semestre, Module, ElementModule, 
#                     CustomUser, Student, Professeur, Admin, Seance, Presence, Planning, AnneUniversitaire.


Faker.seed(321)
fake = Faker('FR_fr')


########### typesalle (amphi et salle)
type_salle_amphi = TypeSalle(1, 500, "Amphi")
type_salle_amphi.save()

type_salle_salle = TypeSalle(2, 50, "Salle")
type_salle_salle.save()
print("insertion de 2 type_salle")


########### Salle (2 salles et 2 amphi)
salle_1 = Salle(1, "I7", True, 1)
salle_1.save()

salle_1 = Salle(2, "I8", False, 1)
salle_1.save()

salle_1 = Salle(3, "Amphi 1", True, 2)
salle_1.save()

salle_1 = Salle(4, "Amphi 4", False, 2)
salle_1.save()
print("insertion de 4 salles")


########### Etablissement (FSTG)
etab = Etablissement(1, "Faculté des Sciences et Techniques Marrakech", "B.P 549, Av.Abdelkarim Elkhattabi, Guéliz Marrakech", "(+212) 524 43 34 04", "Enseignement supérieur", "http://www.fstg-marrakech.ac.ma/FST/", "contact@fstg-marrakech.com", "logo_fstg.png")
etab.save()
print("insertion de 1 etablissement")


########### FILIERE (IRISI, SDAD, SIR)	
irisi = Filiere(1, "IRISI", "logo.png", 1)
irisi.save()

sdad = Filiere(2, "SDAD", "logo.png", 1)
sdad.save()

sir = Filiere(3, "SIR", "logo.png", 1)
sir.save()
print("insertion de 3 filieres")


########### NIVEAU (2 niveaux / filière)	
irisi_N1 = Niveau(1, "IRISI_1", "ingénierie", 1)
irisi_N1.save()

irisi_N2 = Niveau(2, "IRISI_2", "ingénierie", 1)
irisi_N2.save()

sdad_N1 = Niveau(3, "SDAD_1", "master", 2)
sdad_N1.save()

sdad_N2 = Niveau(4, "SDAD_2", "master", 2)
sdad_N2.save()

sir_N1 = Niveau(5, "SIR", "licence", 3)
sir_N1.save()
print("insertion de 5 niveaux")


########### GROUPE 	(1~2 groupes / niveau)
irisi1 = Groupe(1, "G1", 1)
irisi1.save()

irisi2 = Groupe(2, "G1", 2)
irisi2.save()

sdad1 = Groupe(3, "G1", 3)
sdad1.save()

sdad2 = Groupe(4, "G1", 4)
sdad2.save()

sir_G1 = Groupe(5, "G1", 5)
sir_G1.save()

sir_G2 = Groupe(6, "G2", 5)
sir_G2.save()
print("insertion de 6 groupes")


########### SEMESTRE (1 semstre / niveau)
tab_semestres = []
s1_irisi = Semestre(1, "S1", 1)
s1_irisi.save()

s4_irisi = Semestre(2, "S4", 2)
s4_irisi.save()

s1_sdad = Semestre(3, "S1", 3)
s1_sdad.save()

s3_sdad = Semestre(4, "S3", 4)
s3_sdad.save()

s5_sir = Semestre(5, "S5", 5)
s5_sir.save()

print("insertion de 5 semestres")


########### MODULE 	(3~5 modules/semestre)
tab_module = [
    "Intelligence artificielle",
    "base de données répartie",
    "Analyse de données",
    "Programmation concurrentielle",
    "Communication",
    "Système d'exploitation",
    "JEE",
    "Conception UML",
    "Méthode agile",
    "administration de base de données",
]
for i in range(4): 
    semestre = Semestre.objects.get(pk = i+1)
    for j in range(fake.random.randint(3,5)):
        module = Module(libelle_module=tab_module[fake.random.randint(0,9)], semestre=semestre , created_at=fake.date(), updated_at=date.today())
        module.save()

########### users_customuser (820 users : 20 profs + 800 students)
# users_students
users_students = []
for i in range(800):
    first_name = fake.first_name()
    last_name = fake.last_name()
    user = CustomUser(username=first_name + " " + last_name + "_" + str(i),
                      password="pbkdf2_sha256$320000$5a2pLmnD2pZdPCvDJVQyFz$LNTXyVuU0/TNXC3NFKMy978wC8BmN0nXN0bobJeGl9M=", 
                      email=last_name + "." + first_name + "@edu.uca.ma",
                      first_name=first_name,
                      last_name=last_name,
                      user_type=3)
    user.save()
    users_students += [user]
    
            
#####################################################
#                    IRISI 2                        #
#####################################################
irisi2_students = [
    {
        "first_name": "F.Ezzahra",
        "last_name": "Kannoufa",
    },    
    {
        "first_name": "Salma",
        "last_name": "Oussahi",
    },
    {
        "first_name": "Reda",
        "last_name": "Firoud",
    },
    
    {
        "first_name": "Hicham",
        "last_name": "Marouni",
    },
    {
        "first_name": "Narjis",
        "last_name": "Bentouhami",
    },
    {
        "first_name": "Abdelhadi",
        "last_name": "Mouzafir",
    },
    {
        "first_name": "Aminatou",
        "last_name": "Hamissou Abdou",
    },
    {
        "first_name": "Sami",
        "last_name": "Jimouh",
    },
    {
        "first_name": "Khadija",
        "last_name": "Ougoud",
    },
    {
        "first_name": "Kaoutar",
        "last_name": "Oubenaddi",
    },
    {
        "first_name": "Youssef",
        "last_name": "Ettafssaoui",
    },
    {
        "first_name": "Ismail",
        "last_name": "Errouk",
    },
    {
        "first_name": "Said",
        "last_name": "Aabilla",
    },
    {
        "first_name": "Zakaria",
        "last_name": "Outhouna",
    },
    {
        "first_name": "Nabil",
        "last_name": "Lamkadam",
    },
    {
        "first_name": "Abdelaziz",
        "last_name": "Aguenchich",
    },
    {
        "first_name": "Bougary",
        "last_name": "Tamega",
    },
    {
        "first_name": "Hajar",
        "last_name": "Safiaeddine",
    },
    {
        "first_name": "nourelhouda",
        "last_name": "raguigue",
    },
    {
        "first_name": "Ahmed",
        "last_name": "ElRhaouti",
    },
  
]


for i in range(19):
    student = irisi2_students[i]
    last_name = student['last_name']
    first_name = student['first_name']
    user = CustomUser(username=first_name+ " " + last_name,
                    password="pbkdf2_sha256$320000$5a2pLmnD2pZdPCvDJVQyFz$LNTXyVuU0/TNXC3NFKMy978wC8BmN0nXN0bobJeGl9M=", 
                    email=last_name + "." + first_name + "@edu.uca.ma",
                    first_name=first_name,
                    last_name=last_name,
                    user_type=3)
    user.save()
    users_students += [user]
    


# users_prof
count = 2
users_prof = []
for i in range(20):   
    first_name = fake.first_name()
    last_name = fake.last_name()
    user = CustomUser(id=count, username=first_name + " " + last_name + "_" + str(i),
                      password="pbkdf2_sha256$320000$5a2pLmnD2pZdPCvDJVQyFz$LNTXyVuU0/TNXC3NFKMy978wC8BmN0nXN0bobJeGl9M=",
                      email=last_name + "." + first_name + "@edu.uca.ma",
                      first_name=first_name,
                      last_name=last_name,
                      user_type=2)
    user.save()
    count +=1
    users_prof += [user]


########### ADMIN 	
admin = Admin(id=1,created_at=fake.date(), updated_at=date.today(), admin_id=1)
admin.save()

########### STUDENTS (800 students)
for i in range(818):
    user = users_students[i]
    student = Students(cne=fake.numerify('EE######'),
                       adresse=fake.address(),
                       path_photos="face_recognition/service_metier/dataset/Etudiant_"+ user.last_name + "_" + user.first_name  +'/',
                       telephone=fake.numerify('06########'),
                       code_apogee=fake.numerify('18#####'),
                       admin_id=1,
                       user_id=user.id,
                       profile_pic="photo.jpg"
                       )      
    student.save()
    


############ PROFESSEUR (20 profs)
for i in range(20):
    #prof = Professeur(matricule=fake.numerify('########'), specialite="Informatique", telephone=fake.numerify('06########'), created_at=fake.date(), updated_at=date.today(), admin_id=users_prof[i].id)
    prof = Professeur(created_at=fake.date(), updated_at=date.today(), admin_id=users_prof[i].id)
    prof.save()
    


############ Element de module (1 element / module)

#id	libelle_element_module	volumeHoraire	objectif	created_at	updated_at	module_id	responsable_id
modules = Module.objects.all()
profs = Professeur.objects.all()
for i in range(13):
    elt_module = ElementModule(i+1, modules[i].libelle_module, volumeHoraire=fake.random.randint(20,30), objectif=fake.text(), created_at=fake.date(), updated_at=date.today(), module_id=modules[i].id, responsable_id=profs[i].id)
    elt_module.save()


############ Planning (1~3 planings / eltModule)
JOURS =["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"]
elts_mod = ElementModule.objects.all()	
for elt in elts_mod:
    for i in range(fake.random.randint(1,3)):
        planning = Planning(libelle=elt.libelle_element_module,
                            groupe_id=fake.random.randint(1,6),
                            professeur_id=profs[i].id,
                            salle_id=fake.random.randint(1,4),
                            element_module_id=elt.id,
                            jour=JOURS[fake.random.randint(0,4)],
                            heure_debut=datetime.time(10, 30, 00),
                            heure_fin=datetime.time(12, 30, 00),
                            )
        planning.save()


############ Seance (8~10 séances / planning)
plannings = Planning.objects.all()	
for planning in plannings:
    for i in range(fake.random.randint(8,10)):
        day = fake.date_this_month()
        seance = Seance(date=day,
                        planning_id=planning.id
                        )
        seance.save()
        
        
############# Students -- Groupe : AnneUniversitaire
#   enregistrement des étudiants d'IRISI2 dans le groupe G1/IRISI_2/IRISI
grp_irisi2 = Groupe.objects.get(niveau__nom_niveau='IRISI_2')
students_irisi2 = Students.objects.filter(id__gte=803)
for student in students_irisi2:
    annee = AnneUniversitaire(
        libelle = '2021/2022',
        date = date.today(),
        etudiant_id	= student.id,
        group_id = grp_irisi2.id,
    )
    annee.save()	

#   enregistrement des autres étudiants dans des groupes aléatoires
groups = Groupe.objects.exclude(niveau__nom_niveau='IRISI_2')
students= Students.objects.filter(id__lte=802)
for student in students:
    annee = AnneUniversitaire(
        libelle = '2021/2022',
        date = date.today(),
        etudiant_id	= student.id,
        group_id = groups[fake.random.randint(0,(groups.count() - 1))].id,
    )
    annee.save()	


############ Presence (enregistrer des présences pour chaque séance)
seances = Seance.objects.all()

for seance in seances:
    # récupérer l'id du grp concerné pour cette séance
    groupe_id = seance.planning.groupe_id
    etudiants_groupes = AnneUniversitaire.objects.filter(group_id=groupe_id)
    for etudiant_grp in etudiants_groupes:
        presence = Presence(libelle="Séance : " + str(seance.date), 
                            etudiant_id=etudiant_grp.etudiant_id, 
                            is_present=fake.boolean(),
                            seance_id=seance.id)
        presence.save()

            
