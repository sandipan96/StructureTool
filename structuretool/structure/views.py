from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import ProjectDetailsForm, MatStrengthForm
from .models import ProjectDetails, SimpleTable, AlloyGrade, MatStrength
from extra_views import CreateWithInlinesView, InlineFormSetFactory


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
    query_result2 = MatStrength.objects.all()
    selectVal = request.GET['alloygrade']
    user = request.user
    alloy = query_results.filter(owner = user)
    matStr = query_result2.filter(owner = user)
    context = {'alloy' : alloy, 'matStr' : matStr,'selectVal' : selectVal}
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
    model2 = MatStrength
    template_name = 'structure/structureCalc.html'

    def get_queryset(self):
        return AlloyGrade.objects.filter(owner = self.request.user)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objects"] = self.model.objects.all().filter(owner = self.request.user)
        context["mats"] = self.model2.objects.all().filter(owner = self.request.user)
        context["selected"] = self.request.POST.get('alloygrade')
        return context
'''
  
'''         

def structSpecs(request,pk):
    return render(request,'structure/structSpecs.html')

def alloyEdit(request,pk):
    query_results = AlloyGrade.objects.all()
    user = request.user
    alloygrades = query_results.filter(owner = user)
    context = {'alloy' : alloygrades}
    return render(request,'structure/alloyEdit.html',context)



class AlloyListView(ListView):
    model = ProjectDetails
    template_name = 'structure/alloyEdit.html'
    context_object_name = 'alloygrades'
    
    def get_queryset(self):
        return AlloyGrade.objects.filter(owner = self.request.user)

class AlloyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = AlloyGrade
    success_url = '/choice/'
    
    def test_func(self):
        alloyGrade = self.get_object()
        if self.request.user == alloyGrade.owner:
            return True
        return False

    #def delete(self, *args, **kwargs):
        #self.object = self.get_object()    
        #super().delete(*args, **kwargs)

    def get_success_url(self):
        alloygrade = self.object.alloygrade
        return reverse_lazy('alloyEdit', kwargs = {'pk' : self.object.id})
