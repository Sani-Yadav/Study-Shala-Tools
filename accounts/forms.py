from django import forms
from .models import UserProfile, CustomUser

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'institution_name', 'class_or_year', 'address', 'city', 'country', 
            'postal_code', 'profile_picture', 'website', 'twitter', 'linkedin', 
            'github', 'email_notifications', 'dark_mode'
        ]

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'user_type']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user