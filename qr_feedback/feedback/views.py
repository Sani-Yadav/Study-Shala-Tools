import qrcode
import base64
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from .models import FeedbackForm, FeedbackResponse
from .forms import FeedbackFormCreateForm
from io import BytesIO
import uuid

def create_form(request):
    if request.method == "POST":
        form = FeedbackFormCreateForm(request.POST)
        if form.is_valid():
            feedback_form = FeedbackForm.objects.create(
                title=form.cleaned_data['title'],
                owner_email=form.cleaned_data['owner_email'],
                slug=str(uuid.uuid4())
            )
            return redirect('feedback:generate_qr', slug=feedback_form.slug)
    else:
        form = FeedbackFormCreateForm()
    return render(request, 'feedback/create_form.html', {'form': form})

def generate_qr(request, slug):
    feedback_form = FeedbackForm.objects.get(slug=slug)
    # Original working URL
    form_url = request.build_absolute_uri(reverse('feedback:submit_feedback', args=[slug]))
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(form_url)
    qr.make(fit=True)
    
    # Create the QR code image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # If it's an AJAX request or direct image request, return the image
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'download' in request.GET:
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        
        if 'download' in request.GET:
            response = HttpResponse(buffer, content_type="image/png")
            response['Content-Disposition'] = f'attachment; filename="feedback_qr_{slug}.png"'
            return response
        else:
            return HttpResponse(buffer, content_type="image/png")
    
    # For normal page view, show the QR code page
    # Generate QR code and convert to base64 for direct embedding
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    qr_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return render(request, 'feedback/qr_code.html', {
        'feedback_form': feedback_form,
        'qr_image_data': f"data:image/png;base64,{qr_image_base64}",
        'form_url': form_url,
        'request': request
    })

def submit_feedback(request, slug):
    try:
        feedback_form = FeedbackForm.objects.get(slug=slug)
    except FeedbackForm.DoesNotExist:
        return HttpResponse("Invalid feedback form", status=404)
    
    if request.method == 'GET':
        return render(request, 'feedback/feedback_form.html', {'form': feedback_form})
    
    elif request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        rating = request.POST.get('rating')
        suggestion = request.POST.get('suggestion', '').strip()
        
        if not name or not email or not rating:
            return render(request, 'feedback/feedback_form.html', {
                'form': feedback_form, 
                'error': 'Name, Email and Rating are required!',
                'name': name,
                'email': email,
                'suggestion': suggestion,
                'rating': rating
            })
        try:
            # Save the feedback response
            response = FeedbackResponse.objects.create(
                form=feedback_form,
                name=name,
                email=email,
                rating=rating,
                suggestion=suggestion
            )
            
            # Send email to form owner (will print to console in development)
            if feedback_form.owner_email:
                    subject = f'New Feedback Received: {feedback_form.title}'
                    message = f"""
                    New feedback has been submitted for your form "{feedback_form.title}":
                    
                    Name: {name}
                    Email: {email}
                    Rating: {rating}/5
                    Suggestion: {suggestion}
                    """
                    
                    send_mail(
                        subject=subject.strip(),
                        message=message.strip(),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[feedback_form.owner_email],
                        fail_silently=True,
                    )
                    
                    # Send confirmation to the submitter
                    if email:
                        confirmation_subject = f'Thank you for your feedback - {feedback_form.title}'
                        confirmation_message = f"""
                        Thank you for your feedback on "{feedback_form.title}".
                        
                        We appreciate you taking the time to share your thoughts with us.
                        
                        Your feedback:
                        Rating: {rating}/5
                        Suggestion: {suggestion}
                        
                        Best regards,
                        {feedback_form.title} Team
                        """
                        
                        send_mail(
                            subject=confirmation_subject.strip(),
                            message=confirmation_message.strip(),
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[email],
                            fail_silently=True,
                        )
                        
        except Exception as e:
            print(f"Error saving feedback: {e}")
            return render(request, 'feedback/feedback_form.html', {
                'form': feedback_form,
                'error': 'An error occurred while saving your feedback. Please try again.',
                'name': name,
                'email': email,
                'suggestion': suggestion,
                'rating': rating
            })
            
        # If everything went well
        return render(request, 'feedback/success.html')
    
    # If not a POST request, show the form
    return render(request, 'feedback/feedback_form.html', {'form': feedback_form})