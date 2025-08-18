from django import forms
from .models import ScannedNote
 
class ScannedNoteForm(forms.ModelForm):
    class Meta:
        model = ScannedNote
        fields = ['title', 'image'] 