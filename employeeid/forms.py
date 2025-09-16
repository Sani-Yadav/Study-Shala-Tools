from django import forms
from .models import Employee
import csv
from io import TextIOWrapper

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'join_date': forms.DateInput(attrs={'type': 'date'}),
        }

class BulkEmployeeForm(forms.Form):
    csv_file = forms.FileField(
        label='CSV File',
        help_text='Upload a CSV file with employee details. Required columns: full_name, employee_id, designation, department, company, contact, email, join_date (YYYY-MM-DD)'
    )
    
    def clean_csv_file(self):
        csv_file = self.cleaned_data['csv_file']
        if not csv_file.name.endswith('.csv'):
            raise forms.ValidationError('File is not a CSV file')
        return csv_file
