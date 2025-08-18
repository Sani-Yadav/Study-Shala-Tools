from django.shortcuts import render, redirect, get_object_or_404


# Create your views here.

from .forms import EmployeeForm
from .models import Employee

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

