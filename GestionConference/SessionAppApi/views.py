from django.shortcuts import render
from rest_framework import viewsets
from .serializers import SessionSerializer 
from SessionApp.models import Session
# Create your views here.

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class= SessionSerializer
