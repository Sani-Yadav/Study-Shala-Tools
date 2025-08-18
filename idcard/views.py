from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import IDCard
from .forms import IDCardForm, BulkIDCardUploadForm
import uuid
import pandas as pd
from datetime import datetime
from django.db import transaction
from django.core.exceptions import ValidationError

def id_card_view(request):
    """View to display ID cards for the current user"""
    if not request.user.is_authenticated:
        messages.warning(request, 'Please log in to view your ID cards.')
        return redirect('login')
        
    # Get all ID cards for the current user
    id_cards = IDCard.objects.filter(user=request.user)
    return render(request, 'idcard/view_card.html', {'id_cards': id_cards})

def create_id_card(request):
    """View to create a new ID card"""
    if request.method == 'POST':
        form = IDCardForm(request.POST, request.FILES)
        if form.is_valid():
            id_card = form.save(commit=False)
            id_card.user = request.user
            
            # Generate a unique Student ID in format: STU-{YEAR}-{COURSE_CODE}-{UNIQUE_ID}
            if not id_card.student_id:
                # Get current year
                current_year = datetime.now().year
                # Get first 2 letters of course (or 'CS' if not available)
                course_code = (id_card.course[:2].upper() if id_card.course else 'CS')
                # Generate unique ID
                unique_id = uuid.uuid4().hex[:8].upper()
                # Create the formatted Student ID
                id_card.student_id = f"STU-{current_year}-{course_code}-{unique_id}"
            
            try:
                id_card.save()
                messages.success(request, 'Your ID card has been created successfully!')
                return redirect('idcard:id_card_view')
            except Exception as e:
                messages.error(request, f'Error creating ID card: {str(e)}')
                return redirect('idcard:create_id_card')
    else:
        # Initialize form without pre-filling student_id (it will be generated on save)
        form = IDCardForm()
    
    return render(request, 'idcard/create_card.html', {'form': form})

def update_id_card(request, card_id=None):
    """View to update an existing ID card"""
    if card_id:
        id_card = get_object_or_404(IDCard, id=card_id)
    else:
        try:
            id_card = request.user.id_card
        except IDCard.DoesNotExist:
            messages.error(request, 'No ID card found to update.')
            return redirect('idcard:id_card_view')
    
    if request.method == 'POST':
        form = IDCardForm(request.POST, request.FILES, instance=id_card)
        if form.is_valid():
            form.save()
            messages.success(request, 'ID card has been updated successfully!')
            return redirect('idcard:id_card_view')
    else:
        form = IDCardForm(instance=id_card)
    
    return render(request, 'idcard/update_card.html', {'form': form})

def delete_id_card(request, card_id):
    """View to delete an ID card"""
    try:
        id_card = IDCard.objects.get(id=card_id)
        id_card.delete()
        messages.success(request, 'ID card deleted successfully.')
    except IDCard.DoesNotExist:
        messages.error(request, 'ID card not found.')
    return redirect('idcard:id_card_view')

def bulk_upload_id_cards(request):
    """View to upload multiple ID cards from Excel file"""
    # Only staff/admin users can access this view
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('idcard:id_card_view')
    
    if request.method == 'POST':
        form = BulkIDCardUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            
            # Get default values from form
            default_college = form.cleaned_data.get('default_college', '')
            default_course = form.cleaned_data.get('default_course', '')
            default_year = form.cleaned_data.get('default_year', '')
            expiry_date = form.cleaned_data.get('expiry_date')
            
            # Process Excel file
            try:
                # Read Excel file
                df = pd.read_excel(excel_file)
                
                # Validate required columns
                required_columns = ['Username', 'First Name', 'Last Name', 'Email', 'Student ID']
                missing_columns = [col for col in required_columns if col not in df.columns]
                
                if missing_columns:
                    messages.error(request, f'Excel file is missing required columns: {", ".join(missing_columns)}')
                    return render(request, 'idcard/bulk_upload.html', {'form': form})
                
                # Track results
                created_count = 0
                skipped_count = 0
                error_count = 0
                error_messages = []
                
                # Process each row in the Excel file
                with transaction.atomic():
                    for index, row in df.iterrows():
                        try:
                            # Get or create user
                            username = str(row['Username']).strip()
                            email = str(row['Email']).strip()
                            first_name = str(row['First Name']).strip()
                            last_name = str(row['Last Name']).strip()
                            student_id = str(row['Student ID']).strip()
                            
                            # Skip if username or student_id is empty
                            if not username or not student_id:
                                skipped_count += 1
                                continue
                            
                            # Check if user exists
                            try:
                                user = User.objects.get(username=username)
                            except User.DoesNotExist:
                                # Create new user
                                user = User.objects.create_user(
                                    username=username,
                                    email=email,
                                    first_name=first_name,
                                    last_name=last_name,
                                    password=f"temp_{uuid.uuid4().hex[:8]}"  # Temporary password
                                )
                            
                            # Check if user already has an ID card
                            if hasattr(user, 'id_card'):
                                skipped_count += 1
                                continue
                            
                            # Get additional fields from Excel or use defaults
                            college = str(row.get('College', default_college)).strip()
                            course = str(row.get('Course', default_course)).strip()
                            year = str(row.get('Year', default_year)).strip()
                            contact_number = str(row.get('Contact Number', '')).strip()
                            address = str(row.get('Address', '')).strip() if 'Address' in row else None
                            
                            # Handle DOB if present
                            dob = None
                            if 'DOB' in row and pd.notna(row['DOB']):
                                try:
                                    dob = pd.to_datetime(row['DOB']).date()
                                except:
                                    pass
                            
                            # Generate Student ID in format: STU-{YEAR}-{COURSE_CODE}-{UNIQUE_ID}
                            current_year = datetime.now().year
                            course_code = (course[:2].upper() if course else 'CS')
                            unique_id = uuid.uuid4().hex[:8].upper()
                            
                            # If student_id is not provided or empty, generate a new one
                            if not student_id:
                                student_id = f"STU-{current_year}-{course_code}-{unique_id}"
                            
                            # Create ID card
                            id_card = IDCard(
                                user=user,
                                student_id=student_id,
                                college=college,
                                course=course,
                                year=year,
                                contact_number=contact_number,
                                address=address,
                                dob=dob,
                                expiry_date=expiry_date,
                                is_active=True
                            )
                            
                            id_card.save()
                            created_count += 1
                            
                        except Exception as e:
                            error_count += 1
                            error_messages.append(f"Row {index+2}: {str(e)}")
                
                # Show results
                if created_count > 0:
                    messages.success(request, f'Successfully created {created_count} ID cards.')
                if skipped_count > 0:
                    messages.info(request, f'Skipped {skipped_count} entries (duplicate usernames or existing ID cards).')
                if error_count > 0:
                    messages.warning(request, f'Encountered {error_count} errors during processing.')
                    for error in error_messages[:10]:  # Show first 10 errors
                        messages.error(request, error)
                    if len(error_messages) > 10:
                        messages.error(request, f'... and {len(error_messages) - 10} more errors')
                
                return redirect('bulk_upload_id_cards')
                
            except Exception as e:
                messages.error(request, f'Error processing Excel file: {str(e)}')
    else:
        form = BulkIDCardUploadForm()
    
    return render(request, 'idcard/bulk_upload.html', {'form': form})
