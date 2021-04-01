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
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import ProjectDetailsForm, MatStrengthForm, SectionLibraryForm
from .models import ProjectDetails, SimpleTable, AlloyGrade, MatStrength, SectionLibrary
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
        return context
        



def alloyEdit(request,pk):
    query_results = AlloyGrade.objects.all()
    project_results = ProjectDetails.objects.all()
    user = request.user
    alloygrades = query_results.filter(owner = user)
    context = {'alloy' : alloygrades}
    return render(request,'structure/alloyEdit.html',context)



class AlloyListView(CreateView):
    model = AlloyGrade
    fields= ["alloygrade"] 
    template_name = 'structure/alloyEdit.html'
    
    def get_queryset(self):
        return AlloyGrade.objects.filter(owner = self.request.user)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objects"] = self.model.objects.all().filter(owner = self.request.user)
        return context    
        

class AlloyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = AlloyGrade
    
    def test_func(self):
        alloyGrade = self.get_object()
        if self.request.user == alloyGrade.owner:
            return True
        return False

    def get_success_url(self):
        alloygrade = self.object.alloygrade
        return reverse_lazy('alloyEdit', kwargs = {'pk' : self.object.id})

def matStrEdit(request,pk):
    query_results = MatStrength.objects.all()
    user = request.user
    matStrFiltered = query_results.filter(owner = user)
    context = {'matStr' : matStrFiltered}
    return render(request,'structure/matStrEdit.html',context)

class MatStrListView(CreateView):
    model = MatStrength
    fields= ["name","bendStress"] 
    template_name = 'structure/matStrEdit.html'
    
    def get_queryset(self):
        return MatStrength.objects.filter(owner = self.request.user)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objects"] = self.model.objects.all().filter(owner = self.request.user)
        return context       

class MatStrDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MatStrength
    
    def test_func(self):
        matStrength = self.get_object()
        if self.request.user == matStrength.owner:
            return True
        return False

    def get_success_url(self):
        matStr = self.object.name
        return reverse_lazy('matStrEdit', kwargs = {'pk' : self.object.id})

def structSpecs(request,pk):
    sections = SectionLibrary.objects.all()
    context = {'sections' : sections}
    return render(request,'structure/structSpecs.html',context)

        
def addSection(request,pk):
    if request.method == 'POST':
        form = SectionLibraryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Added a new Section!')
            return redirect('/choice/projectList/')
        else:
            messages.success(request, f'Failed!!!')     
    else:
        form = SectionLibraryForm()   

    context = {
        'form' : form
    }   
    return render(request, 'structure/addSection.html', context)


  