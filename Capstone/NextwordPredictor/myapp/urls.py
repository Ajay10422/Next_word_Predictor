from django.urls import path
from . import views

urlpatterns = [
    path('', views.input_text, name='input_text'),
    
]