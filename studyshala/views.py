from django.shortcuts import render
from notes.models import Note
from django.contrib.auth import get_user_model
from employeeid.models import Employee

def home(request):
    # Get the custom user model
    User = get_user_model()
    
    # Get some statistics for the home page
    notes_count = Note.objects.count()
    users_count = User.objects.count()
    
    # Get recent notes
    recent_notes = Note.objects.all().order_by('-uploaded_at')[:6]
    
    # Get the first employee for preview
    try:
        employee = Employee.objects.first()
    except:
        employee = None
    
    context = {
        'notes_count': notes_count,
        'users_count': users_count,
        'recent_notes': recent_notes,
        'employee': employee,
    }
    return render(request, 'home.html', context)
