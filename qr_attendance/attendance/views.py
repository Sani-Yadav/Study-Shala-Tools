from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
import csv
from .models import AttendanceSession, AttendanceRecord, Student
from .utils import generate_qr
import uuid

def generate_attendance_qr(request):
    # create a new session with random id
    session_id = str(uuid.uuid4())
    session = AttendanceSession.objects.create(session_id=session_id)
    qr_img = generate_qr(session_id)
    return render(request, 'attendance/qr_display.html', {'qr_img': qr_img, 'session_id': session_id})

def attendance_mark(request):
    if request.method == 'POST':
        session_id = request.POST.get('session_id', '').strip()
        roll_no = request.POST.get('roll_no', '').strip()
        student_name = request.POST.get('student_name', '').strip()
        
        # Validate inputs
        if not all([session_id, roll_no, student_name]):
            return render(request, 'attendance/mark_result.html', {
                'msg': 'Error: All fields are required (Session ID, Roll Number, and Name)',
                'is_error': True
            })
        
        try:
            # Get or create student
            student, student_created = Student.objects.get_or_create(
                roll_no=roll_no,
                defaults={'name': student_name}  # Use provided name for new student
            )
            
            # Update name if student exists but name is different
            if not student_created and student.name != student_name:
                student.name = student_name
                student.save()
            
            # Get session
            session = AttendanceSession.objects.filter(session_id=session_id).first()
            if not session:
                return render(request, 'attendance/mark_result.html', {
                    'msg': f'Error: Invalid Session ID: {session_id}',
                    'is_error': True
                })
            
            # Check if attendance already marked
            if AttendanceRecord.objects.filter(student=student, session=session).exists():
                return render(request, 'attendance/mark_result.html', {
                    'msg': f'Attendance already marked for {roll_no}',
                    'is_error': False
                })
                
            # Mark attendance
            AttendanceRecord.objects.create(student=student, session=session)
            return render(request, 'attendance/mark_result.html', {
                'msg': f'Attendance marked successfully for {roll_no}!',
                'is_error': False
            })
            
        except Exception as e:
            return render(request, 'attendance/mark_result.html', {
                'msg': f'Error: {str(e)}',
                'is_error': True
            })
    
    # Handle GET request - show the attendance form
    return render(request, 'attendance/mark_attendance.html')

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
from django.utils import timezone

def download_attendance_records(request, session_id=None):
    # First, get all students
    all_students = Student.objects.all()
    
    # If session_id is provided, filter by that session, otherwise get all records
    if session_id:
        session = get_object_or_404(AttendanceSession, session_id=session_id)
        records = AttendanceRecord.objects.filter(session=session).select_related('student', 'session')
        report_title = f"Attendance Report - Session: {session_id}"
    else:
        # Get all attendance records across all sessions
        records = AttendanceRecord.objects.all().select_related('student', 'session')
        report_title = "Complete Attendance Report - All Sessions"
    
    # Create a dictionary to store attendance for each student
    student_records = {}
    
    # Initialize all students with empty records
    for student in all_students:
        student_records[(student.roll_no, student.name)] = {
            'count': 0,
            'records': []
        }
    
    # Now add the attendance records
    for record in records:
        key = (record.student.roll_no, record.student.name)
        if key not in student_records:
            student_records[key] = {'count': 0, 'records': []}
            
        student_records[key]['count'] += 1
        student_records[key]['records'].append({
            'timestamp': record.timestamp,
            'session_id': record.session.session_id
        })
    
    # Debug: Print number of records found
    print(f"Found {records.count()} attendance records")
    
    # Count attendance for each student
    attendance_count = {}
    for record in records:
        key = (record.student.roll_no, record.student.name)
        attendance_count[key] = attendance_count.get(key, 0) + 1
    
    # Create a BytesIO buffer for the PDF file
    buffer = BytesIO()
    
    # Create the PDF object, using the BytesIO object as its "file."
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Add title
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=20,
        alignment=1  # Center alignment
    )
    
    elements.append(Paragraph(report_title, title_style))
    if session_id:
        elements.append(Paragraph(f"Session ID: {session_id}", styles['Normal']))
        elements.append(Paragraph(f"Date: {session.date.strftime('%Y-%m-%d')}", styles['Normal']))
    elements.append(Spacer(1, 20))
    
    # Prepare data for the table
    data = [
        ['Roll Number', 'Student Name', 'Attendance Count', 'Last Attendance Time']
    ]
    
    # Sort students by roll number for consistent ordering
    sorted_students = sorted(student_records.items(), key=lambda x: x[0][0])  # Sort by roll number
    
    
    print(f"\nGrouped {len(student_records)} unique students")
    
    # Add student data to table with all timestamps
    for (roll_no, name), record_data in sorted_students:
        # Sort records by timestamp (newest first)
        sorted_records = sorted(record_data['records'], key=lambda x: x['timestamp'], reverse=True)
        
        # Format all timestamps with session info
        if sorted_records:
            timestamps_str = '\n'.join(
                f"{rec['timestamp'].strftime('%Y-%m-%d %H:%M:%S')} (Session: {rec['session_id']})"
                for rec in sorted_records
            )
        else:
            timestamps_str = "No attendance recorded"
        
        data.append([
            roll_no,
            name,
            str(record_data['count']),
            timestamps_str
        ])
    
    # Create the table
    table = Table(data)
    
    # Add style to the table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (2, -1), 'CENTER'),  # Align first 3 columns center
        ('ALIGN', (3, 0), (3, -1), 'LEFT'),    # Align timestamps left
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),   # Align content to top of cell
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8),  # Slightly smaller font for better fit
        ('LEADING', (0, 1), (-1, -1), 12),  # Line spacing for multi-line cells
    ])
    
    table.setStyle(style)
    elements.append(table)
    
    # Add summary
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(
        f"Total Students: {len(student_records)}", 
        styles['Normal']
    ))
    
    # Build the PDF
    doc.build(elements)
    
    # File response
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="attendance_report_{session_id}.pdf"'
    
    return response
    
    return render(request, 'attendance/mark_attendance.html')
