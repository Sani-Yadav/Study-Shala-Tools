from django import forms
from .models import UserProfile, JobApplication

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'dob', 'address', 'photo']

class JobApplicationForm(forms.Form):
    job_title = forms.CharField(max_length=255)
