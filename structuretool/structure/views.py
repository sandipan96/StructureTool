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


        
    query = SectionLibrary.objects.all()
    context = {'sections': sections,'sectionNames':sectionNames, 'query':query, 'alloygrade':alloygrade, 'alloystrength':alloystrength,
                'bendStress': bendStress, 'maxDeflection': maxDeflection, 'windLoad': windLoad, 'shapeChoice' : shapeChoice, 'liCoef':liCoef,
                'mdCoef':mdCoef, 'length':length, 'lwidth':lwidth, 'rwidth':rwidth}
    return render(request,'structure/sectionView.html',context)



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
    liCoefSession = request.session['liCoefSession']
    mdCoefSession = request.session['mdCoefSession']
    shapeChoiceSession = request.session['shapeChoiceSession']
    query_result = ProjectDetails.objects.get(pk = pk)
    today = date.today()
    if request.method == 'POST':
        system = request.POST.get('sectionview')
        systemName = request.POST.get('sectionNames')
        ixx = request.POST.get('property1')
        wxx = request.POST.get('property2')
        sectionDrawing = request.POST.get('sectionDrawing')

    finalMaxDefl = 0
    maxDefl = (float(lengthSession)/float(maxDeflectionSession)) * 1000
    if maxDefl < float(maxDeflection2Session):
        finalMaxDefl = maxDefl
    else:
        finalMaxDefl = maxDeflection2Session

    finalMaxDefl = float(finalMaxDefl)/10
    finalMaxDeflRounded = round(finalMaxDefl,2)

    loadWidth = (float(lwidthSession)/2) + (float(rwidthSession)/2)
    windPressure = float(windLoadSession) * 0.000010197162129779
    w = windPressure * loadWidth * 100
    
    diagramPath = ""

     #change based on shape
    
    print(shapeChoiceSession)
    #Rectangular
    if shapeChoiceSession == "Rectangular":
        momentInertia = (5 * w * (float(lengthSession) * 100)**4)/(384 * 700000 * finalMaxDefl)
        momentInertiaRounded = round(momentInertia,2)    
        fActual = (5 * w * (float(lengthSession) * 100)**4)/(384 * 700000 * float(ixx))
        fActualRounded = round(fActual,2)
        maxBendMoment = (w * (float(lengthSession) * 100) ** 2)/8
        maxBendMomentRounded = round(maxBendMoment,2)
        diagramPath = "D:\MyProjects\\tool\structuretool\structure\static\structure\deflRectangle.JPG"
    elif shapeChoiceSession == "Trapezoidal":
        #Triangle ( need to double check)
        if float(lengthSession) <= float(lwidthSession) and float(lengthSession) <= float(rwidthSession):
            momentInertia = (w * (float(lengthSession) * 100)**4) / (60 * 700000 * finalMaxDefl)
            print(momentInertia)
            momentInertiaRounded = round(momentInertia,2) 
            fActual = (w * (float(lengthSession) * 100)**4) / (60 * 700000 * float(ixx))
            fActualRounded = round(fActual,2)
            maxBendMoment = (w * (float(lengthSession) * 100))/6
            maxBendMomentRounded = round(maxBendMoment,2)
            diagramPath = "D:/MyProjects/tool/structuretool/structure/static/structure/deflTriangle.JPG"  
        else:
            #Trapezoidal ( need to double check)
            momentInertia = (w * (float(lengthSession) * 100)**4 * (25-(40 * (float(lwidthSession)/(float(lengthSession))**2) + (16 * (float(lwidthSession)/(float(lengthSession))**4)))))/(1920 * 700000 * finalMaxDefl)
            momentInertiaRounded = round(momentInertia,2) 
            fActual = (w * (float(lengthSession) * 100)**4 * (25-(40 * (float(lwidthSession)/(float(lengthSession))**2) + (16 * (float(lwidthSession)/(float(lengthSession))**4)))))/(1920 * 700000 * float(ixx))
            maxBendMoment = 1000
            maxBendMomentRounded = round(maxBendMoment,2)
            fActualRounded = round(fActual,2)
            diagramPath = "D:\MyProjects\\tool\structuretool\structure\static\structure\deflDummy.JPG"
    print(diagramPath)
    

    inertiaSatisfied = "OKAY"
    inertiaSign = ">"

    if float(ixx) < momentInertia:
        inertiaSatisfied = "NOT OKAY"
        inertiaSign = "<"

   
    
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

    fig = go.Figure()
    fig.update_xaxes(
        range = [0,(float(lengthSession) * 100) + 50 ],
        zeroline = False,
    )
    fig.update_yaxes(
        range = [0,maxBendMoment],
        zeroline = False,
    )
    paths = "M 0,0 Q {},{} {},0".format((float(lengthSession) * 100)/2,maxBendMoment*2,float(lengthSession) * 100)
    fig.update_layout(
        title = "Bending Moment Diagram under design wind load",
        xaxis_title = "Unsupported Length in cm",
        yaxis_title = "Bending Moment kg-cm",
        shapes = [
            dict(
                type = "path",
                path = paths,
                line_color="RoyalBlue",
            ),
        ],
    )
    fig.add_hline(y = maxBendMoment, line_dash = "dash")
    fig.write_image("structure/static/structure/fig.jpeg")


    fig1 = go.Figure()
    fig1.update_xaxes(
        range = [0,(float(lengthSession) * 100) + 50 ],
        zeroline = False,
    )
    fig1.update_yaxes(
        range = [0,fActual + (fActual/10)],
        zeroline = False,
    )
    paths1 = "M 0,0 Q {},{} {},0".format((float(lengthSession) * 100)/2,fActual*2,float(lengthSession) * 100)
    fig1.update_layout(
        title = "Deflection Diagram under design wind load",
        xaxis_title = "Unsupported Length in cm",
        yaxis_title = "Deflection in cm",
        shapes = [
            dict(
                type = "path",
                path = paths1,
                line_color="Red",
            ),
        ]
    )
    fig1.add_hline(y = fActual, line_dash = "dash")
    fig1.write_image("structure/static/structure/fig1.jpeg")

    serviceMoment = maxBendMoment * float(liCoefSession)
    serviceMomentRounded = round(serviceMoment,2)

    maxPermStress = float(bendStressSession) / float(mdCoefSession)
    maxPermStressRounded = round(maxPermStress,2)

    actualBendStress = serviceMoment / float(wxx)
    actualBendStressRounded = round(actualBendStress, 2)
    stressSign = "<"
    stressSatisfied = "OKAY"
    if actualBendStress > maxPermStress :
        stressSign = ">"
        stressSatisfied = "NOT OKAY"
        
    sectionMod = serviceMoment / maxPermStress
    sectionModRounded = round(sectionMod, 2)

    sectionModSign = "<"
    sectionModSatisfied = "OKAY"
    if sectionMod > float(wxx):
        sectionModSign = ">"
        sectionModSatisfied = "NOT OKAY"

    ultimateCriteria = "satisfied"
    if stressSatisfied == "NOT OKAY" or sectionModSatisfied == "NOT OKAY":
        ultimateCriteria = "not satisfied"

    query_drawing = SectionLibrary.objects.get(sectionName = systemName)
    context = {'alloygradeSession':alloygradeSession, 'alloyStrengthSession': alloyStrengthSession, 'bendStressSession': bendStressSession, 'shapeChoiceSession':shapeChoiceSession,
                'lengthSession': lengthSession, 'lwidthSession' : lwidthSession, 'rwidthSession' : rwidthSession, 'system':system, 'systemName':systemName, 
                'maxDeflectionSession': maxDeflectionSession, 'maxDeflection2Session': maxDeflection2Session,'ixx':ixx, 'wxx':wxx, 'sectionDrawing':sectionDrawing, 'query_result':query_result, 
                'query_drawing' : query_drawing, 'today':today, 'finalMaxDeflRounded' : finalMaxDeflRounded, 'momentInertiaRounded':momentInertiaRounded,'inertiaSatisfied':inertiaSatisfied,
                'inertiaSign':inertiaSign, 'fActualRounded':fActualRounded,'deflSatisfied':deflSatisfied,'deflSign':deflSign,'deflCriteria':deflCriteria, 'maxBendMomentRounded' : maxBendMomentRounded,
                'liCoefSession': liCoefSession, 'mdCoefSession': mdCoefSession, 'serviceMomentRounded': serviceMomentRounded, 'maxPermStressRounded' : maxPermStressRounded,
                'stressSign': stressSign, 'stressSatisfied': stressSatisfied, 'actualBendStressRounded':actualBendStressRounded, 'sectionModRounded':sectionModRounded, 'sectionModSign': sectionModSign,
                'sectionModSatisfied' : sectionModSatisfied, 'ultimateCriteria':ultimateCriteria, 'diagramPath':diagramPath} 
                
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


    



  