from django import template
 #*@author ABDELHADI MOUZAFIR END
 
register = template.Library()

@register.filter
def to_and(value):
    return value.replace(" ","_")