from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'structure-home'),
    path('choice/', views.choicePage, name = 'structure-choice'),
]