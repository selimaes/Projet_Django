from django.shortcuts import render
from .models import Conference
from django.views.generic import ListView , DetailView 
from django.views.generic.edit import CreateView , UpdateView , DeleteView
from django.urls import reverse_lazy
from .forms import ConferenceModel


def all_conferences(req):
    conferences = Conference.objects.all()
    return render(req , 'conference/liste.html', {'liste': conferences})

class ConferenceList(ListView):
    
    model=Conference
    context_object_name='liste'
    ordering = ['-start_date']
    template_name= 'conference/liste.html'
    
class ConferenceDetails(DetailView):
    model=Conference
    context_object_name="conference"
    ordering = ['-start_date']
    template_name= 'conference/detail.html'

class ConferenceCreate(CreateView):
    model=Conference
    template_name="conference/conference_forms.html"
    #fields='__all__'
    form_class=ConferenceModel
    success_url=reverse_lazy("conference_liste")
    
class ConferenceUpdate(UpdateView):
    model= Conference
    template_name='conference/conference_forms.html'
    #fields='__all__'
    form_class=ConferenceModel
    success_url=reverse_lazy("conference_liste")
    
class ConferenceDelete(DeleteView):
    model= Conference
    template_name= "conference/conference_confirm_delete.html"
    success_url=reverse_lazy("conference_liste")
    