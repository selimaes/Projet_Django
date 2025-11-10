from django.shortcuts import render
from .models import Conference
from django.views.generic import ListView , DetailView 
from django.views.generic.edit import CreateView , UpdateView , DeleteView
from django.urls import reverse_lazy
from .forms import ConferenceModel
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Submission
from .forms import SubmissionForm 
from django.shortcuts import redirect


class ListSubmissions(LoginRequiredMixin, ListView):
    model = Submission
    template_name = "conference/list_submissions.html"  # à créer
    context_object_name = "submissions"
    ordering = ['-submission_date']

    def get_queryset(self):
        # On filtre pour ne prendre que les submissions de l'utilisateur connecté
        return Submission.objects.filter(user_id=self.request.user)



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

class ConferenceCreate(LoginRequiredMixin,CreateView):
    model=Conference
    template_name="conference/conference_forms.html"
    #fields='__all__'
    form_class=ConferenceModel
    success_url=reverse_lazy("conference_liste")
    
class ConferenceUpdate(LoginRequiredMixin,UpdateView):
    model= Conference
    template_name='conference/conference_forms.html'
    #fields='__all__'
    form_class=ConferenceModel
    success_url=reverse_lazy("conference_liste")
    
class ConferenceDelete(LoginRequiredMixin,DeleteView):
    model= Conference
    template_name= "conference/conference_confirm_delete.html"
    success_url=reverse_lazy("conference_liste")
    


class ListeSubmissions(LoginRequiredMixin, ListView):
    model = Submission
    template_name = "conference/liste_submissions.html" 
    context_object_name = "submissions"
    ordering = ['-submission_date']

   
    


class SubmissionDetail(LoginRequiredMixin, DetailView):
    model = Submission
    template_name = "conference/submission_detail.html"  
    context_object_name = "submission"



 

class AddSubmission(LoginRequiredMixin, CreateView):
    model = Submission
    template_name = "conference/add_submission.html"  # à créer
    form_class = SubmissionForm
    success_url = reverse_lazy('list_submissions')  # redirection après ajout

    def form_valid(self, form):
        # Associer automatiquement la soumission à l'utilisateur connecté
        form.instance.user_id = self.request.user
        return super().form_valid(form)
    

class UpdateSubmission(LoginRequiredMixin, UpdateView):
    model = Submission
    template_name = "conference/update_submission.html" 
    form_class = SubmissionForm 
    success_url = reverse_lazy('liste_submissions')

    def get_queryset(self):
        # L'utilisateur ne peut modifier que ses propres soumissions
        return Submission.objects.filter(user_id=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        submission = self.get_object()
     
        if submission.status in ['Accepted', 'Rejected']:
            return redirect('liste_submissions')
        return super().dispatch(request, *args, **kwargs)

