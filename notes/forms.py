from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'subject', 'file', 'level']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter note title'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Mathematics, Physics, etc.'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
        } 