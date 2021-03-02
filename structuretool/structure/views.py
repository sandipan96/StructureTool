from django.shortcuts import render
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import ProjectDetailsForm
from .models import ProjectDetails, SimpleTable, AlloyGrade


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

class ProjectDetailView(UserPassesTestMixin, DetailView):
    model = ProjectDetails
    def test_func(self):
        projectDetail = self.get_object()
        if self.request.user == projectDetail.owner:
            return True
        return False  

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = ProjectDetails
    fields= ["projectCode","projectName","clientName","clientEmail","clientPhone","clientAddress"] 

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ProjectDetails
    fields= ["projectCode","projectName","clientName","clientEmail","clientPhone","clientAddress"] 

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        projectDetail = self.get_object()
        if self.request.user == projectDetail.owner:
            return True
        return False  

class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ProjectDetails
    success_url = '/choice/projectList/'
    def test_func(self):
        projectDetail = self.get_object()
        if self.request.user == projectDetail.owner:
            return True
        return False              

def structureCalc(request,pk):
    query_results = AlloyGrade.objects.all()
    user = request.user
    alloy = query_results.filter(owner = user)
    context = {'alloy' : alloy}
    return render(request,'structure/structureCalc.html', context)

# class AlloyListView(ListView):
#     model = AlloyGrade
#     template_name = 'structure/structureCalc.html'
#     context_object_name = 'filtered_alloy'
    
#     def get_queryset(self):
#         return AlloyGrade.objects.filter(owner = self.request.user)

class AlloyListCreate(LoginRequiredMixin, CreateView):
    model = AlloyGrade
    fields= ["alloygrade"] 
    template_name = 'structure/structureCalc.html'

    def get_queryset(self):
        return AlloyGrade.objects.filter(owner = self.request.user)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objects"] = self.model.objects.all().filter(owner = self.request.user)
        return context
