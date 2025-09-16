from django import forms

class FeedbackFormCreateForm(forms.Form):
    title = forms.CharField(max_length=200, label="Form Title")
    owner_email = forms.EmailField(
        label="Your Email",
        help_text="You'll receive notifications at this email when someone submits feedback"
    )