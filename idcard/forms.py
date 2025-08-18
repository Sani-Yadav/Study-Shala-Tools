from django import forms
from .models import IDCard

class IDCardForm(forms.ModelForm):
    class Meta:
        model = IDCard
        fields = [
            'Full_Name', 'student_id', 'college', 'course', 'year',
            'contact_number', 'address', 'dob', 'expiry_date', 'photo', 'is_active'
        ]
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'Full_Name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'student_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Roll No. / Registration ID'}),
            'college': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'College / School Name'}),
            'course': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'BCA, BTech, B.Com etc.'}),
            'year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Current Academic Year / Batch'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'WhatsApp Number Preferred'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'City, State, Country', 'rows': 3}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address'].required = False
        self.fields['dob'].required = False


class BulkIDCardUploadForm(forms.Form):
    excel_file = forms.FileField(
        label='Excel File',
        help_text='Upload an Excel file (.xlsx) with student data. The file must have columns for: Username, First Name, Last Name, Email, Student ID, College, Course, Year, Contact Number, Address (optional), DOB (optional)',
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.xlsx'})
    )
    default_college = forms.CharField(
        max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Default College/School Name'}),
        help_text='If provided, this will be used when the Excel file has empty college values'
    )
    default_course = forms.CharField(
        max_length=50, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Default Course'}),
        help_text='If provided, this will be used when the Excel file has empty course values'
    )
    default_year = forms.CharField(
        max_length=20, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Default Year/Batch'}),
        help_text='If provided, this will be used when the Excel file has empty year values'
    )
    expiry_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        help_text='If provided, all generated ID cards will have this expiry date'
    )