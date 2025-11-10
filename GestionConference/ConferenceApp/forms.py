from django import forms 
from .models import Conference

from .models import Submission



class ConferenceModel(forms.ModelForm):
    class Meta:
        model=Conference
        fields =['name','theme','description','location','start_date','end_date']
        labels = {
            'name':"nom de la conférence",
            'theme':"Thématiques",
            'description':"description",
            'location':"location",
            'start_date':"date debut de la conférence",
            'end_date':"date fin de la conférence",
        }
        widgets ={
            'name': forms.TextInput(attrs={'placeholder':'entrez le titre de la conferene'}),
            'location': forms.TextInput(attrs={'placeholder':'entrez le lieu'}),
            
            'start_date' : forms.DateInput(
                attrs= {
                    'type':'date',
                    'placeholder': "date de debut"
                }
            ),
            'end_date' : forms.DateInput(
                attrs={
                    'type':'date',
                    'placeholder':"date de fin"
                }
            )     
        }
        
        
      

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['title', 'abstract', 'keywords', 'paper', 'conference_id', 'status', 'payed']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'conference_id': forms.Select(attrs={'class': 'form-select'}),
            'keywords': forms.TextInput(attrs={'placeholder': 'Séparer les mots-clés par des virgules'}),
            'abstract': forms.Textarea(attrs={'rows': 4}),
        }



class UpdateSubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['title', 'abstract', 'keywords', 'paper']
        widgets = {
            'keywords': forms.TextInput(attrs={'placeholder': 'Séparer les mots-clés par des virgules'}),
            'abstract': forms.Textarea(attrs={'rows': 4}),
        }
        
