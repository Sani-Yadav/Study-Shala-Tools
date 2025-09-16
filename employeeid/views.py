from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.views.generic import CreateView
from django.urls import reverse_lazy

# Create your views here.
from .forms import EmployeeForm, BulkEmployeeForm
from .models import Employee
import csv
from io import TextIOWrapper
from django.contrib import messages
from django.db import transaction

class CreateEmployeeCardView(CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employeeid/create_employee_card.html'
    success_url = reverse_lazy('employeeid:upload_employee')
    
    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, 'Employee ID card created successfully!')
        return redirect('employeeid:employee_card', pk=self.object.pk)

def upload_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            employee = form.save()
            return redirect('employeeid:employee_card', pk=employee.pk)
    else:
        form = EmployeeForm()
    return render(request, 'employeeid/upload.html', {'form': form})

def employee_card(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employeeid/id_card.html', {'employee': employee})

def update_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employeeid:employee_card', pk=employee.pk)
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employeeid/update_employee.html', {'form': form, 'employee': employee})

def bulk_upload_employee(request):
    if request.method == 'POST':
        form = BulkEmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = TextIOWrapper(
                request.FILES['csv_file'].file,
                encoding=request.encoding or 'utf-8'
            )
            reader = csv.DictReader(csv_file)
            
            required_fields = ['full_name', 'employee_id', 'designation', 
                             'department', 'company', 'contact', 'email', 'join_date']
            
            # Check if all required fields are present
            if not all(field in reader.fieldnames for field in required_fields):
                messages.error(request, 'CSV file is missing required columns')
                return redirect('employeeid:bulk_upload')
            
            success_count = 0
            errors = []
            
            with transaction.atomic():
                for i, row in enumerate(reader, 1):
                    try:
                        employee = Employee(
                            full_name=row['full_name'],
                            employee_id=row['employee_id'],
                            designation=row['designation'],
                            department=row['department'],
                            company=row['company'],
                            contact=row['contact'],
                            email=row['email'],
                            join_date=row['join_date'],
                            # Add a default profile image or handle it separately
                            profile_image='employee_photos/default.png'
                        )
                        employee.save()
                        success_count += 1
                    except Exception as e:
                        errors.append(f"Row {i}: {str(e)}")
            
            if success_count > 0:
                messages.success(request, f'Successfully imported {success_count} employees')
            if errors:
                messages.warning(request, f'Encountered {len(errors)} errors during import')
                for error in errors[:5]:  # Show first 5 errors to avoid message flooding
                    messages.warning(request, error)
                if len(errors) > 5:
                    messages.warning(request, f'... and {len(errors) - 5} more errors')
            
            return redirect('employeeid:bulk_upload')
    else:
        form = BulkEmployeeForm()
    
    return render(request, 'employeeid/bulk_upload.html', {'form': form})

def delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, 'Employee record deleted successfully.')
        return redirect('employeeid:upload_employee')
    return redirect('employeeid:employee_card', pk=pk)

