from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import redirect
from xhtml2pdf import pisa
from .models import (
    Resume, 
    Experience, 
    Education, 
    Project, 
    Certification, 
    Achievement, 
    Reference
)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse


def test_pdf(request):
    """Test PDF generation with minimal template"""
    from django.template.loader import render_to_string
    from xhtml2pdf import pisa
    
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="test.pdf"'
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('PDF generation failed')
    return response

def generate_pdf(request, resume_id, template_type='simple'):
    try:
        # Get the resume with all related data in a single query
        resume = Resume.objects.select_related('user').prefetch_related(
            'experiences', 'education_entries', 'projects',
            'certifications', 'achievements', 'references'
        ).get(id=resume_id)
        
        # Select template based on type - fix template paths
        templates = {
            'simple': 'resume/simple_resume.html',
            'professional': 'resume/professional_resume.html',  # Fixed path
            'modern': 'resume/simple_resume.html'
        }
        template_path = templates.get(template_type, 'resume/simple_resume.html')
        
        # Process skills and languages into lists
        def process_skills(skills_str):
            if not skills_str:
                return []
            return [skill.strip() for skill in skills_str.split(',') if skill.strip()]
            
        # Prepare context with all resume data
        context = {
            'resume': resume,
            'profile_image_url': resume.profile_image.url if resume.profile_image else None,
            'technical_skills': process_skills(resume.technical_skills),
            'soft_skills': process_skills(resume.soft_skills),
            'languages': process_skills(resume.languages),
            'hobbies': process_skills(resume.hobbies),
            'base_url': request.build_absolute_uri('/').rstrip('/'),
        }

        # Render template
        template = get_template(template_path)
        html = template.render(context)

        # Create PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{resume.full_name or "resume"}_Resume.pdf"'
        
        # Simple PDF generation with minimal options
        pisa_status = pisa.CreatePDF(
            html,
            dest=response,
            encoding='utf-8',
            link_callback=lambda uri, _: uri,
        )

        if pisa_status.err:
            # Log the error for debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"PDF generation error: {pisa_status.log}")
            return HttpResponse('PDF generation failed. Please try again or contact support.')

        return response
        
    except Resume.DoesNotExist:
        return HttpResponse('Resume not found', status=404)
    except Exception as e:
        # Log the full error for debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"PDF generation error: {str(e)}")
        return HttpResponse(f'An error occurred: {str(e)}', status=500)
        return HttpResponse(f'An error occurred: {str(e)}', status=500)

@login_required
def simple_builder(request, resume_id=None):
    """
    Simple resume builder view that allows users to create and edit their resume
    """
    # Get or create resume for the current user
    if resume_id:
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    else:
        resume, created = Resume.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Handle form submission
        try:
            # Update basic info
            resume.full_name = request.POST.get('full_name', '')
            resume.job_title = request.POST.get('job_title', '')
            resume.email = request.POST.get('email', '')
            resume.phone = request.POST.get('phone', '')
            resume.location = request.POST.get('location', '')
            resume.github = request.POST.get('github', '')
            resume.portfolio_url = request.POST.get('portfolio_url', '')
            resume.summary = request.POST.get('summary', '')
            resume.technical_skills = request.POST.get('technical_skills', '')
            resume.soft_skills = request.POST.get('soft_skills', '')
            resume.languages = request.POST.get('languages', '')
            
            # Handle profile image upload
            if 'profile_image' in request.FILES:
                resume.profile_image = request.FILES['profile_image']
            
            resume.save()
            
            # Handle experience entries
            _handle_experience_entries(request, resume)
            
            # Handle education entries
            _handle_education_entries(request, resume)
            
            # Handle projects
            _handle_projects(request, resume)
            
            messages.success(request, 'Resume saved successfully!')
            return redirect('resume:simple_builder', resume_id=resume.id)
            
        except Exception as e:
            messages.error(request, f'Error saving resume: {str(e)}')
    
    return render(request, 'resume/simple_builder.html', {'resume': resume})

def _handle_experience_entries(request, resume):
    """Handle experience entries from the form"""
    # Update existing experiences
    for exp in resume.experiences.all():
        exp_id = str(exp.id)
        exp.job_title = request.POST.get(f'exp_title_{exp_id}', '')
        exp.company = request.POST.get(f'exp_company_{exp_id}', '')
        exp.duration = request.POST.get(f'exp_duration_{exp_id}', '')
        exp.description = request.POST.get(f'exp_description_{exp_id}', '')
        exp.save()
    
    # Add new experiences
    i = 0
    while True:
        if f'new_exp_title_{i}' not in request.POST:
            break
            
        job_title = request.POST.get(f'new_exp_title_{i}')
        if job_title:  # Only add if there's a job title
            Experience.objects.create(
                resume=resume,
                job_title=job_title,
                company=request.POST.get(f'new_exp_company_{i}', ''),
                duration=request.POST.get(f'new_exp_duration_{i}', ''),
                description=request.POST.get(f'new_exp_description_{i}', '')
            )
        i += 1

def _handle_education_entries(request, resume):
    """Handle education entries from the form"""
    # Update existing education entries
    for edu in resume.education_entries.all():
        edu_id = str(edu.id)
        edu.degree = request.POST.get(f'edu_degree_{edu_id}', '')
        edu.institution = request.POST.get(f'edu_institution_{edu_id}', '')
        edu.year = request.POST.get(f'edu_year_{edu_id}', '')
        edu.description = request.POST.get(f'edu_description_{edu_id}', '')
        edu.save()
    
    # Add new education entries
    i = 0
    while True:
        if f'new_edu_degree_{i}' not in request.POST:
            break
            
        degree = request.POST.get(f'new_edu_degree_{i}')
        if degree:  # Only add if there's a degree
            Education.objects.create(
                resume=resume,
                degree=degree,
                institution=request.POST.get(f'new_edu_institution_{i}', ''),
                year=request.POST.get(f'new_edu_year_{i}', ''),
                description=request.POST.get(f'new_edu_description_{i}', '')
            )
        i += 1

def _handle_projects(request, resume):
    """Handle project entries from the form"""
    # Update existing projects
    for proj in resume.projects.all():
        proj_id = str(proj.id)
        proj.title = request.POST.get(f'project_title_{proj_id}', '')
        proj.tech_stack = request.POST.get(f'project_tech_{proj_id}', '')
        proj.description = request.POST.get(f'project_description_{proj_id}', '')
        proj.live_url = request.POST.get(f'project_url_{proj_id}', '')
        proj.save()
    
    # Add new projects
    i = 0
    while True:
        if f'new_project_title_{i}' not in request.POST:
            break
            
        title = request.POST.get(f'new_project_title_{i}')
        if title:  # Only add if there's a title
            Project.objects.create(
                resume=resume,
                title=title,
                tech_stack=request.POST.get(f'new_project_tech_{i}', ''),
                description=request.POST.get(f'new_project_description_{i}', ''),
                live_url=request.POST.get(f'new_project_url_{i}', '')
            )
        i += 1

@login_required
def upload_resume(request):
    return render(request, 'resume/upload_resume.html')


@login_required
def preview_resume(request):
    """
    View to preview the resume before saving
    """
    if request.method == 'POST':
        # Process form data from POST request
        return render(request, 'resume/preview.html', {
            'resume_data': request.POST
        })
    else:
        # Try to get data from session storage (for preview button)
        resume_data = request.session.get('resume_data')
        if resume_data:
            return render(request, 'resume/preview.html', {
                'resume_data': resume_data
            })
        return redirect('resume:builder')

@login_required
def builder(request, template_type='simple', resume_id=None):
    """
    View for the resume builder page with template selection
    """
    if resume_id:
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    else:
        # Try to get existing resume or create new one
        resume = Resume.objects.filter(user=request.user).first()
        if not resume:
            resume = Resume.objects.create(
                user=request.user,
                full_name=request.user.get_full_name() or request.user.username,
                email=request.user.email or ''
            )
            return redirect('resume:builder_template_with_id', template_type=template_type, resume_id=resume.id)
        
    context = {
        'template_type': template_type,
        'resume': resume,
        'resume_id': resume.id if resume else None,
    }
    
    if request.user.is_authenticated:
        if not resume:
            resume, created = Resume.objects.get_or_create(
                user=request.user,
                defaults={
                    'full_name': request.user.get_full_name() or request.user.username,
                    'email': request.user.email or ''
                }
            )
        
            
        
    
    if request.method == 'POST':
        # Handle form submission with all fields
        resume_data = {
            'full_name': request.user.get_full_name() or request.user.username,
            'email': request.user.email
        }
        
        # Handle profile image upload
        if 'profile_image' in request.FILES:
            resume_data['profile_image'] = request.FILES['profile_image']
        
        # Create or update resume
        resume, created = Resume.objects.update_or_create(
            user=request.user if request.user.is_authenticated else None,
            defaults=resume_data
        )
        
        # Get project data from form
        project_titles = request.POST.getlist('project_title[]', [])
        project_descriptions = request.POST.getlist('project_description[]', [])
        tech_stacks = request.POST.getlist('tech_stack[]', [])
        project_links = request.POST.getlist('project_link[]', [])
        
        # Handle Experience
        job_titles = request.POST.getlist('job_title[]', [])
        companies = request.POST.getlist('company[]', [])
        job_durations = request.POST.getlist('job_duration[]', [])
        job_descriptions = request.POST.getlist('job_description[]', [])
        
        # Handle Education
        degrees = request.POST.getlist('degree[]', [])
        institutions = request.POST.getlist('institution[]', [])
        education_durations = request.POST.getlist('education_duration[]', [])
        education_descriptions = request.POST.getlist('education_description[]', [])
        
        # Clear existing data
        resume.projects.all().delete()
        resume.experiences.all().delete()
        resume.education_entries.all().delete()
        
        # Save experiences
        for i in range(len(job_titles)):
            if job_titles[i]:
                Experience.objects.create(
                    resume=resume,
                    job_title=job_titles[i],
                    company=companies[i] if i < len(companies) else '',
                    duration=job_durations[i] if i < len(job_durations) else '',
                    description=job_descriptions[i] if i < len(job_descriptions) else ''
                )
        
        # Save education
        for i in range(len(degrees)):
            if degrees[i]:
                Education.objects.create(
                    resume=resume,
                    degree=degrees[i],
                    institution=institutions[i] if i < len(institutions) else '',
                    duration=education_durations[i] if i < len(education_durations) else '',
                    description=education_descriptions[i] if i < len(education_descriptions) else ''
                )
        
        # Save projects
        for i in range(len(project_titles)):
            if project_titles[i]:
                Project.objects.create(
                    resume=resume,
                    title=project_titles[i],
                    description=project_descriptions[i] if i < len(project_descriptions) else '',
                    tech_stack=tech_stacks[i] if i < len(tech_stacks) else '',
                    live_url=project_links[i] if i < len(project_links) else ''
                )
        
        # Handle Certifications
        cert_titles = request.POST.getlist('cert_title[]')
        platforms = request.POST.getlist('platform[]')
        cert_years = request.POST.getlist('cert_year[]')
        
        # Clear existing certifications
        resume.certifications.all().delete()
        
        # Add new certifications
        for i in range(len(cert_titles)):
            if cert_titles[i]:
                Certification.objects.create(
                    resume=resume,
                    title=cert_titles[i],
                    platform=platforms[i] if i < len(platforms) else '',
                    year=cert_years[i] if i < len(cert_years) else ''
                )
        
        # Handle Achievements
        achievements = request.POST.getlist('achievement[]')
        
        # Clear existing achievements
        resume.achievements.all().delete()
        
        # Add new achievements
        for achievement in achievements:
            if achievement.strip():
                Achievement.objects.create(
                    resume=resume,
                    description=achievement.strip()
                )
        
        # Handle References
        ref_names = request.POST.getlist('ref_name[]')
        ref_relationships = request.POST.getlist('ref_relationship[]')
        ref_contacts = request.POST.getlist('ref_contact[]')
        
        # Clear existing references
        resume.references.all().delete()
        
        # Add new references
        for i in range(len(ref_names)):
            if ref_names[i]:
                Reference.objects.create(
                    resume=resume,
                    name=ref_names[i],
                    relationship=ref_relationships[i] if i < len(ref_relationships) else '',
                    contact_info=ref_contacts[i] if i < len(ref_contacts) else ''
                )
        
        # Check if this is a save and download request
        if 'save_and_download' in request.POST:
            # Redirect to the generate_pdf view
            return redirect('resume:generate_pdf', resume_id=resume.id, template_type=template_type)
        
        # After saving all data, redirect to prevent form resubmission
        return redirect('resume:builder')
    
    # For GET request, render the form with resume data
    context = {
        'resume': resume,
        'template_type': template_type,
        'experiences': resume.experiences.all() if resume else [],
        'education_entries': resume.education_entries.all() if resume else [],
        'projects': resume.projects.all() if resume else [],
        'certifications': resume.certifications.all() if resume else [],
        'achievements': resume.achievements.all() if resume else [],
        'references': resume.references.all() if resume else [],
    }
    return render(request, 'resume/builder.html', context)
