from django import forms
from .models import ProjectDetails, MatStrength

class ProjectDetailsForm(forms.ModelForm):
    class Meta:
        model= ProjectDetails
        fields= ["owner","projectCode","projectName","clientName","clientEmail","clientPhone","clientAddress"]

class MatStrengthForm(forms.ModelForm):
    class Meta:
        model = MatStrength
        fields = ["owner","name","bendStress"]
