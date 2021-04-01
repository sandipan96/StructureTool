from django.urls import path
from . import views
from .views import (
    ProjectListView, 
    ProjectDetailView, 
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
    AlloyListCreate,
    AlloyListView,
    AlloyDeleteView,
    MatStrListView,
    MatStrDeleteView,
)

urlpatterns = [
    path('', views.home, name = 'structure-home'),
    path('choice/', views.choicePage, name = 'structure-choice'),
    path('choice/projectList/',ProjectListView.as_view(), name = 'projectList'),
    path('choice/projectList/<int:pk>/',ProjectDetailView.as_view(), name = 'ProjectDetails-detail'),
    path('choice/projectList/<int:pk>/update/',ProjectUpdateView.as_view(), name = 'ProjectDetails-update'),
    path('choice/projectList/<int:pk>/delete/',ProjectDeleteView.as_view(), name = 'ProjectDetails-delete'),
    path('choice/projectList/new/',ProjectCreateView.as_view(), name = 'ProjectDetails-create'),
    path('choice/projectList/<int:pk>/structureCalc/',AlloyListCreate.as_view(), name = 'structureCalc'),
    path('choice/projectList/<int:pk>/structureCalc/alloyEdit/',AlloyListView.as_view(), name = 'alloyEdit'),
    path('choice/projectList/<int:pk>/structureCalc/alloyEdit/delete/',AlloyDeleteView.as_view(), name = 'AlloyGrade-delete'),
    path('choice/projectList/<int:pk>/structureCalc/structSpecs/',views.structSpecs, name = 'structSpecs'),
    path('choice/projectList/<int:pk>/structureCalc/structSpecs/addSection/',views.addSection, name = 'addSection'),
    path('choice/projectList/<int:pk>/structureCalc/matStrEdit/',MatStrListView.as_view(), name = 'matStrEdit'),
    path('choice/projectList/<int:pk>/structureCalc/matStrEdit/delete',MatStrDeleteView.as_view(), name = 'MatStrength-delete'),
]