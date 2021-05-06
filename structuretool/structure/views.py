import os
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
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import ProjectDetailsForm, MatStrengthForm, SectionLibraryForm, SectionFormTwo
from .models import ProjectDetails, SimpleTable, AlloyGrade, MatStrength, SectionLibrary
from extra_views import CreateWithInlinesView, InlineFormSetFactory
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.contrib.staticfiles import finders
from datetime import date
import numpy as np
import plotly.graph_objects as go


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
    
    # self.request.session['alloystrength'] = alloyStrength
    # self.request.session['bendstress'] = bendStress
    # self.request.session['maxDeflection'] = maxDeflection
    # self.request.session['windLoad'] = windLoad
    # self.request.session['shapeChoice'] = shapeChoice
    # self.request.session['liCoef'] = liCoef
    # self.request.session['mdCoef'] = mdCoef
    # self.request.session['length'] = length
    # self.request.session['lwidth'] = lwidth
    # self.request.session['rwidth'] = rwidth


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
        request.session['alloygradeSession'] = alloygrade
        alloystrength = request.POST.get('alloyStrength')
        request.session['alloyStrengthSession'] = alloystrength
        bendStress = request.POST.get('bendStress')
        request.session['bendStressSession'] = bendStress
        maxDeflection = request.POST.get('maxDeflection')
        request.session['maxDeflectionSession'] = maxDeflection
        maxDeflection2 = request.POST.get('maxDeflection2')
        request.session['maxDeflection2Session'] = maxDeflection2
        windLoad = request.POST.get('windLoad')
        request.session['windLoadSession'] = windLoad
        shapeChoice = request.POST.get('shapeChoice')
        request.session['shapeChoiceSession'] = shapeChoice
        liCoef = request.POST.get('liCoef')
        request.session['liCoefSession'] = liCoef
        mdCoef = request.POST.get('mdCoef')
        request.session['mdCoefSession'] = mdCoef
        length = request.POST.get('length')
        request.session['lengthSession'] = length
        lwidth = request.POST.get('lwidth')
        request.session['lwidthSession'] = lwidth
        rwidth = request.POST.get('rwidth')
        request.session['rwidthSession'] = rwidth

        
    # np.random.seed(1)

    # N = 100
    # x = np.random.rand(N)
    # y = np.random.rand(N)
    # colors = np.random.rand(N)
    # sz = np.random.rand(N) * 30

    # fig = go.Figure()
    # fig.add_trace(go.Scatter(
    #     x=x,
    #     y=y,
    #     mode="markers",
    #     marker=go.scatter.Marker(
    #         size=sz,
    #         color=colors,
    #         opacity=0.6,
    #         colorscale="Viridis"
    #     )
    # ))
    # fig.write_image("structure/static/structure/fig1.jpeg")

        
    query = SectionLibrary.objects.all()
    context = {'sections': sections,'sectionNames':sectionNames, 'query':query, 'alloygrade':alloygrade, 'alloystrength':alloystrength,
                'bendStress': bendStress, 'maxDeflection': maxDeflection, 'windLoad': windLoad, 'shapeChoice' : shapeChoice, 'liCoef':liCoef,
                'mdCoef':mdCoef, 'length':length, 'lwidth':lwidth, 'rwidth':rwidth}
    return render(request,'structure/sectionView.html',context)

# def link_callback(uri, rel):
#             """
#             Convert HTML URIs to absolute system paths so xhtml2pdf can access those
#             resources
#             """
#             result = finders.find(uri)
#             if result:
#                     if not isinstance(result, (list, tuple)):
#                             result = [result]
#                     result = list(os.path.realpath(path) for path in result)
#                     path=result[0]
#             else:
#                     sUrl = settings.STATIC_URL        # Typically /static/
#                     sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
#                     mUrl = settings.MEDIA_URL         # Typically /media/
#                     mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

#                     if uri.startswith(mUrl):
#                             path = os.path.join(mRoot, uri.replace(mUrl, ""))
#                     elif uri.startswith(sUrl):
#                             path = os.path.join(sRoot, uri.replace(sUrl, ""))
#                     else:
#                             return uri

#             # make sure that file exists
#             if not os.path.isfile(path):
#                     raise Exception(
#                             'media URI must start with %s or %s' % (sUrl, mUrl)
#                     )
#             return path

def windowsPDF(request,pk):
    template_path = "structure/windowsPDF.html"
    alloygradeSession = request.session['alloygradeSession']
    alloyStrengthSession = request.session['alloyStrengthSession']
    bendStressSession = request.session['bendStressSession']
    windLoadSession = request.session['windLoadSession']
    maxDeflectionSession = request.session['maxDeflectionSession']
    maxDeflection2Session = request.session['maxDeflection2Session']
    lengthSession = request.session['lengthSession']
    lwidthSession = request.session['lwidthSession'] 
    rwidthSession = request.session['rwidthSession']
    query_result = ProjectDetails.objects.get(pk = pk)
    today = date.today()

    finalMaxDefl = 0
    maxDefl = (float(lengthSession)/float(maxDeflectionSession)) * 1000
    if maxDefl < float(maxDeflection2Session):
        finalMaxDefl = maxDefl
    else:
        finalMaxDefl = maxDeflection2Session

    finalMaxDefl = finalMaxDefl/10
    finalMaxDeflRounded = round(finalMaxDefl,2)

    loadWidth = (float(lwidthSession)/2) + (float(rwidthSession)/2)
    windPressure = float(windLoadSession) * 0.000010197162129779
    w = windPressure * loadWidth * 100
    momentInertia = (5 * w * (float(lengthSession) * 100)**4)/(384 * 700000 * finalMaxDefl)
    momentInertiaRounded = round(momentInertia,2) 

    if request.method == 'POST':
        system = request.POST.get('sectionview')
        systemName = request.POST.get('sectionNames')
        ixx = request.POST.get('property1')
        wxx = request.POST.get('property2')
        sectionDrawing = request.POST.get('sectionDrawing')

    inertiaSatisfied = "OKAY"
    inertiaSign = ">"

    if float(ixx) < momentInertia:
        inertiaSatisfied = "NOT OKAY"
        inertiaSign = "<"

    fActual = (5 * w * (float(lengthSession) * 100)**4)/(384 * 700000 * float(ixx))
    fActualRounded = round(fActual,2)

    deflSatisfied = "OKAY"
    deflSign = "<"

    if fActual > finalMaxDefl:
        deflSatisfied = "NOT OKAY"
        deflSign = ">"

    deflCriteria = ""

    if (deflSatisfied == "OKAY" and inertiaSatisfied == "OKAY"):
        deflCriteria = "CRITERIA SATISFIED"
    else:
        deflCriteria = "CRITERIA NOT SATISFIED"

    maxBendMoment = (w * (float(lengthSession) * 100) ** 2)/8
    
    query_drawing = SectionLibrary.objects.get(sectionName = systemName)
    context = {'alloygradeSession':alloygradeSession, 'alloyStrengthSession': alloyStrengthSession, 'bendStressSession': bendStressSession, 
                'lengthSession': lengthSession, 'lwidthSession' : lwidthSession, 'rwidthSession' : rwidthSession, 'system':system, 'systemName':systemName, 
                'maxDeflectionSession': maxDeflectionSession, 'maxDeflection2Session': maxDeflection2Session,'ixx':ixx, 'wxx':wxx, 'sectionDrawing':sectionDrawing, 'query_result':query_result, 
                'query_drawing' : query_drawing, 'today':today, 'finalMaxDeflRounded' : finalMaxDeflRounded, 'momentInertiaRounded':momentInertiaRounded,'inertiaSatisfied':inertiaSatisfied,
                'inertiaSign':inertiaSign, 'fActualRounded':fActualRounded,'deflSatisfied':deflSatisfied,'deflSign':deflSign,'deflCriteria':deflCriteria, 'maxBendMoment' : maxBendMoment}
                
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


    



  