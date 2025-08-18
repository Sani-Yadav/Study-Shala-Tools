from django.shortcuts import render, get_object_or_404
from notes.models import Note
from django.contrib.auth import get_user_model
from employeeid.models import Employee  # Assuming Employee model exists in employeeid app

def home(request):
    # Get the custom user model
    User = get_user_model()
    
    # Get some statistics for the home page
    notes_count = Note.objects.count()
    users_count = User.objects.count()
    
    # Get recent notes
    recent_notes = Note.objects.all().order_by('-uploaded_at')[:6]
    
    # Get employee data if user is authenticated
    employee = None
    if request.user.is_authenticated:
        try:
            employee = Employee.objects.filter(user=request.user).first()
        except Exception:
            # Handle case if Employee model doesn't exist
            pass
    
    context = {
        'notes_count': notes_count,
        'users_count': users_count,
        'recent_notes': recent_notes,
        'employee': employee,
    }
    return render(request, 'home.html', context)
