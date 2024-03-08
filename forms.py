from django import forms
from .models import Course, Grade 


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course 
        fields =("nom", "prof", "classe", "heures", "maximum", "fiche", "utilisateur")
        widgets = {
            'nom':forms.TextInput(attrs={'class':'form-control'}),
            'prof': forms.TextInput(attrs={'class':'form-control'}),
            'classe': forms.Select(attrs={'class':'form-control'}),
            'heures': forms.TextInput(attrs={'class':'form-control', 'type':'number'}),
            'maximum': forms.TextInput(attrs={'class':'form-control', 'type':'number'}),
            'utilisateur': forms.TextInput(attrs={'class':'form-control'}),
        }

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields =("nom", "createur", "liste_eleves")
        widgets = {
            'nom':forms.TextInput(attrs={'class':'form-control'}),
          }
        