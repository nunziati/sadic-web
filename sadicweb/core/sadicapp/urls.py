from django.urls import path
from . import views
from .views import upload_pdb, get_progress

urlpatterns = [
    path('', views.upload_pdb, name='upload_pdb'),
    path('progress/', get_progress, name='progress'),
]
