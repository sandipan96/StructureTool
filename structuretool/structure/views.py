from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import Context
from .forms import ProjectDetailsForm
from .models import ProjectDetails, SimpleTable


def home(request):
    return render(request, 'structure/home.html')

@login_required
def choicePage(request):
    return render(request, 'structure/choice.html')

@login_required
def windowOne(request):
    form = ProjectDetailsForm(request.POST)
    if form.is_valid():
        form.save()
    context = {'form' : form}    
    return render(request, 'structure/windowOne.html', context)

@login_required
def viewProjectTable(request):
    query_results = ProjectDetails.objects.all()
    user = request.user
    filtered_results = query_results.filter(owner = user)
    table = SimpleTable(filtered_results)
    context = {'table' : table}
    return render(request, 'structure/projectTable.html', context)