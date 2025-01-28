from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_pdb, name='upload_pdb'),
]