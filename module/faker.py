import os 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "helloworld.settings")

import django 
django.setup() 

from faker import factory,Faker 
from  filiere.models import *

fake = Faker() 

# ! generate dummy data for testing 
   # ! code here <>