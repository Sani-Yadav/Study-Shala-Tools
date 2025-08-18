from django.shortcuts import render, redirect, get_object_or_404
from .forms import ScannedNoteForm
from .models import ScannedNote
from PIL import Image
import pytesseract
from reportlab.pdfgen import canvas
from django.core.files.base import ContentFile
from io import BytesIO

# Create your views here.

def scan_note(request):
    if request.method == 'POST':
        form = ScannedNoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)

            # OCR
            image = Image.open(note.image)
            text = pytesseract.image_to_string(image)
            note.extracted_text = text

            # PDF Generation
            buffer = BytesIO()
            p = canvas.Canvas(buffer)
            p.drawString(100, 800, note.title)
            y = 780
            for line in text.splitlines():
                p.drawString(100, y, line)
                y -= 15
            p.save()
            buffer.seek(0)
            note.pdf_file.save(f"{note.title}.pdf", ContentFile(buffer.read()), save=False)

            note.save()
            return redirect('scanner:note_detail', pk=note.pk)
    else:
        form = ScannedNoteForm()
    return render(request, 'scanner/scan_note.html', {'form': form})

def note_detail(request, pk):
    note = get_object_or_404(ScannedNote, pk=pk)
    return render(request, 'scanner/note_detail.html', {'note': note})
