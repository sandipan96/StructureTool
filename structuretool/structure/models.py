from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.urls import reverse
import django_tables2 as tables

class ProjectDetails(models.Model):
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    projectCode = models.IntegerField()
    projectName = models.CharField(max_length = 100)
    clientName  = models.CharField(max_length = 100)
    clientEmail = models.EmailField()
    clientPhone = models.CharField(max_length = 15)
    clientAddress = models.CharField(max_length = 100)

    def __str__(self):
        return self.projectName

    def get_absolute_url(self):
        return reverse('ProjectDetails-detail', kwargs = {'pk' : self.pk})    


class SimpleTable(tables.Table):
    class Meta:
        model = ProjectDetails


class AlloyGrade(models.Model):
    alloygrade = models.CharField(max_length = 20)
    owner = models.ForeignKey(User, on_delete = models.CASCADE)


