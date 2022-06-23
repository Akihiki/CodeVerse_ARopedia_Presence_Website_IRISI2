# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms


class FiliereForm(forms.Form):
    nom_filiere = forms.CharField(max_length=30)
    logo = forms.ImageField(required=False)
