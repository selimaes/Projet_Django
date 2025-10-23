from django.urls import path
from .views import *
#from . import views 
urlpatterns =[
    #path("liste/" ,views.all_conferences,name="conference_liste"),
    path("liste/" , ConferenceList.as_view(), name= "conference_liste"),
    path("details/<int:pk>", ConferenceDetails.as_view(),name="conference_detail")
]
