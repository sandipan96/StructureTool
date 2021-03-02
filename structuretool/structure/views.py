from django.shortcuts import render
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView
)
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProjectDetailsForm
from .models import ProjectDetails, SimpleTable


def home(request):
    return render(request, 'structure/home.html')

@login_required
def choicePage(request):
    return render(request, 'structure/choice.html')

@login_required
def projectList(request):
    query_results = ProjectDetails.objects.all()
    user = request.user
    filtered_results = query_results.filter(owner = user)
    #table = SimpleTable(filtered_results)
    #context = {'table' : table}
    context = {'filtered' : filtered_results}
    return render(request, 'structure/projectList.html', context)   


class ProjectListView(ListView):
    model = ProjectDetails
    template_name = 'structure/projectList.html'
    context_object_name = 'filtered_results'
    
    def get_queryset(self):
        return ProjectDetails.objects.filter(owner = self.request.user)

class ProjectDetailView(DetailView):
    model = ProjectDetails

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = ProjectDetails
    fields= ["projectCode","projectName","clientName","clientEmail","clientPhone","clientAddress"] 

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


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