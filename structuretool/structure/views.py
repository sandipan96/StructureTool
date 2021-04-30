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
from .forms import ProjectDetailsForm, MatStrengthForm, SectionLibraryForm, SectionFormTwo
from .models import ProjectDetails, SimpleTable, AlloyGrade, MatStrength, SectionLibrary
from extra_views import CreateWithInlinesView, InlineFormSetFactory
from xhtml2pdf import pisa
from django.template.loader import get_template


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
    model3 = SectionLibrary
    template_name = 'structure/structureCalc.html'

    def get_queryset(self):
        return AlloyGrade.objects.filter(owner = self.request.user)

    # def post(self, request, *args, **kwargs):
    #     self.request.session['alloygrade'] = form.cleaned_data["alloygrade"]
    #     self.request.session['alloystrength'] = form.cleaned_data["alloyStrength"]
    #     self.request.session['bendstress'] = form.cleaned_data["bendStress"]
    #     self.request.session['maxDeflection'] = form.cleaned_data["maxDeflection"]
    #     self.request.session['windLoad'] = form.cleaned_data["windLoad"]
    #     self.request.session['shapeChoice'] = form.cleaned_data["shapeChocie"]
    #     self.request.session['liCoef'] = form.cleaned_data["liCoef"]
    #     self.request.session['mdCoef'] = form.cleaned_data["mdCoef"]
    #     self.request.session['length'] = form.cleaned_data["length"]
    #     self.request.session['lwidth'] = form.cleaned_data["lwidth"]
    #     self.request.session['rwidth'] = form.cleaned_data["rwidth"]
    #     return render(request, self.template_name, {'form': form})



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

# def structSpecs(request,pk):
#     sections = SectionLibrary.objects.all()
#     context = {'sections' : sections}
#     return render(request,'structure/structSpecs.html',context)

class SectionListCreate(CreateView):
    model = SectionLibrary
    fields= ["system","profileCodeInner","profileCodeOuter","addReinfInner","addReinfOuter","addInserts","drawing","ixx","wxx","sectionName"]    
    template_name = 'structure/structSpecs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sections"] = self.model.objects.all()
        return context

    def get_success_url(self):
        sectionRow = self.object.system
        return reverse_lazy('structSpecs', kwargs = {'pk' : self.object.id})
          

class SectionDeleteView(UserPassesTestMixin, DeleteView):
    model = SectionLibrary    

    def get_success_url(self):
        sectionRow = self.object.system
        return reverse_lazy('structSpecs', kwargs = {'pk' : self.object.id})

    def test_func(self):
        return self.request.user.is_superuser      

class SectionUpdateView(UserPassesTestMixin, UpdateView):
    model = SectionLibrary
    fields= ["system","profileCodeInner","profileCodeOuter","addReinfInner","addReinfOuter","addInserts","drawing","ixx","wxx","sectionName"]

    def test_func(self):
        return self.request.user.is_superuser    
 

def sectionView(request,pk):
    sections = SectionLibrary.objects.values_list("system", flat = True).distinct()
    sectionNames = SectionLibrary.objects.values_list("sectionName")
    if request.method == 'POST':
        alloygrade = request.POST.get('alloygrade')
        alloystrength = request.POST.get('alloyStrength')
        bendstress = request.POST.get('bendStress')
        maxDeflection = request.POST.get('maxDeflection')
        windLoad = request.POST.get('windLoad')
        shapeChoice = request.POST.get('shapeChoice')
        liCoef = request.POST.get('liCoef')
        mdCoef = request.POST.get('mdCoef')
        length = request.POST.get('length')
        lwidth = request.POST.get('lwidth')
        rwidth = request.POST.get('rwidth')
        
    query = SectionLibrary.objects.all()
    context = {'sections': sections,'sectionNames':sectionNames, 'query':query, 'alloygrade':alloygrade, 'alloystrength':alloystrength,
                'bendstress': bendstress, 'maxDeflection': maxDeflection, 'windLoad': windLoad, 'shapeChoice' : shapeChoice, 'liCoef':liCoef,
                'mdCoef':mdCoef, 'length':length, 'lwidth':lwidth, 'rwidth':rwidth}
    return render(request,'structure/sectionView.html',context)



def windowsPDF(request,pk):
    template_path = "structure/windowsPDF.html"

    if request.method == 'POST':
        alloygrade = request.POST.get('alloygrade')
        alloystrength = request.POST.get('alloyStrength')
        bendstress = request.POST.get('bendStress')
        maxDeflection = request.POST.get('maxDeflection')
        windLoad = request.POST.get('windLoad')
        shapeChoice = request.POST.get('shapeChoice')
        liCoef = request.POST.get('liCoef')
        mdCoef = request.POST.get('mdCoef')
        length = request.POST.get('length')
        lwidth = request.POST.get('lwidth')
        rwidth = request.POST.get('rwidth')
        
    
    context = {'alloygrade':alloygrade, 'alloystrength':alloystrength,
                'bendstress': bendstress, 'maxDeflection': maxDeflection, 'windLoad': windLoad, 'shapeChoice' : shapeChoice, 'liCoef':liCoef,
                'mdCoef':mdCoef, 'length':length, 'lwidth':lwidth, 'rwidth':rwidth}
                
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


    



  