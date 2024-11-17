from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    #the best form
    path("<str:name>", views.greet, name= "greet"),
    path("lucas", views.lucas, name = "lucas")
]