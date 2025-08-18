from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Note
from .forms import NoteForm

def notes_list(request):
    notes = Note.objects.all().order_by('-uploaded_at')
    
    # Filtering
    level = request.GET.get('level')
    subject = request.GET.get('subject')
    
    if level:
        notes = notes.filter(level=level)
    if subject:
        notes = notes.filter(subject__icontains=subject)
    
    # Pagination
    paginator = Paginator(notes, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'levels': Note.LEVELS,
        'current_level': level,
        'current_subject': subject,
    }
    return render(request, 'notes/notes_list.html', context)

def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    return render(request, 'notes/note_detail.html', {'note': note})

@login_required
def upload_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.uploaded_by = request.user
            note.save()
            messages.success(request, 'Note uploaded successfully!')
            return redirect('notes:note_detail', note_id=note.id)
    else:
        form = NoteForm()
    
    return render(request, 'notes/upload_note.html', {'form': form})

@login_required
def my_notes(request):
    notes = Note.objects.filter(uploaded_by=request.user).order_by('-uploaded_at')
    return render(request, 'notes/my_notes.html', {'notes': notes})

@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, uploaded_by=request.user)
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note deleted successfully!')
        return redirect('notes:my_notes')
    return render(request, 'notes/delete_note.html', {'note': note})