from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'structure-home'),
    path('choice/', views.choicePage, name = 'structure-choice'),
    path('choice/windowOne/', views.windowOne, name = 'windowOne'),
    path('choice/windowOne/projectTable/', views.viewProjectTable, name = 'projectTable'),
]