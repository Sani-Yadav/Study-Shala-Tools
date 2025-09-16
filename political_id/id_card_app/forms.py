from django import forms
from .models import IDCard

class IDCardForm(forms.ModelForm):
    class Meta:
        model = IDCard
        fields = ['name', 'mobile', 'photo', 'digital_signature']