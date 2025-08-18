from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from .models import Resume, Education, Experience, Project, Certification, Achievement, Reference

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = [
            'profile_image', 'full_name', 'email', 'phone', 'location',
            'linkedin', 'github', 'portfolio_url', 'summary',
            'technical_skills', 'soft_skills', 'languages', 'hobbies'
        ]
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': ''}),
            'technical_skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Python, JavaScript, Django, React, etc.'}),
            'soft_skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teamwork, Communication, Leadership, etc.'}),
            'languages': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'English (Fluent), Spanish (Basic), etc.'}),
            'hobbies': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reading, Hiking, Photography, etc.'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control'}),
            'github': forms.URLInput(attrs={'class': 'form-control'}),
            'portfolio_url': forms.URLInput(attrs={'class': 'form-control'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'profile_image': 'Upload a professional profile picture (optional)',
            'linkedin': 'Your LinkedIn profile URL (optional)',
            'github': 'Your GitHub profile URL (optional)',
            'portfolio_url': 'Your portfolio website URL (optional)',
            'technical_skills': 'Separate skills with commas',
            'soft_skills': 'Separate skills with commas',
            'languages': 'List languages you speak and proficiency level',
        }

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        exclude = ('resume',)

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        exclude = ('resume',)

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ('resume',)

class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        exclude = ('resume',)

class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        exclude = ('resume',)

class ReferenceForm(forms.ModelForm):
    class Meta:
        model = Reference
        exclude = ('resume',)

EducationFormSet = inlineformset_factory(Resume, Education, form=EducationForm, extra=1, can_delete=True)
ExperienceFormSet = inlineformset_factory(Resume, Experience, form=ExperienceForm, extra=1, can_delete=True)
ProjectFormSet = inlineformset_factory(Resume, Project, form=ProjectForm, extra=1, can_delete=True)
CertificationFormSet = inlineformset_factory(Resume, Certification, form=CertificationForm, extra=1, can_delete=True)
AchievementFormSet = inlineformset_factory(Resume, Achievement, form=AchievementForm, extra=1, can_delete=True)
ReferenceFormSet = inlineformset_factory(Resume, Reference, form=ReferenceForm, extra=1, can_delete=True)
