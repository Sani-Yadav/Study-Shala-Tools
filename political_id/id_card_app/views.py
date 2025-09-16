import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import RedirectView
from .models import IDCard
from .forms import IDCardForm

def home(request):
    return redirect('id_card_app:create_id_card')

def create_id_card(request):
    if request.method == 'POST':
        form = IDCardForm(request.POST, request.FILES)
        if form.is_valid():
            id_card = form.save()
            return redirect('id_card_app:show_id_card', pk=id_card.pk)
    else:
        form = IDCardForm()
    
    return render(request, 'id_form.html', {'form': form})

def show_id_card(request, pk):
    id_card = IDCard.objects.get(pk=pk)
    
    # Create QR code with ID card details (simple text format for better scanning)
    qr_data = f"""
    मिशन जारी टीम
    ID: {id_card.id_no}
    नाम: {id_card.name}
    मोबाइल: {id_card.mobile}
    जारी तिथि: {id_card.issued_date}
    """
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save QR code to a BytesIO object
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    qr_code_data = buffer.getvalue()
    
    # Convert to base64 for embedding in HTML
    import base64
    qr_code_base64 = base64.b64encode(qr_code_data).decode('utf-8')
    
    return render(request, 'id_card_display.html', {
        'id_card': id_card,
        'qr_code': qr_code_base64
    })