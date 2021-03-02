from django.urls import path
from . import views
from .views import (
    ProjectListView, 
    ProjectDetailView, 
    ProjectCreateView
)

urlpatterns = [
    path('', views.home, name = 'structure-home'),
    path('choice/', views.choicePage, name = 'structure-choice'),
    path('choice/projectList/',ProjectListView.as_view(), name = 'projectList'),
    path('choice/projectList/<int:pk>/',ProjectDetailView.as_view(), name = 'ProjectDetails-detail'),
    path('choice/projectList/new/',ProjectCreateView.as_view(), name = 'ProjectDetails-create'),
    path('choice/windowOne/', views.windowOne, name = 'windowOne'),
    path('choice/windowOne/projectTable/', views.viewProjectTable, name = 'projectTable'),
]