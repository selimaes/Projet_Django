from django import forms 
from .models import Conference



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