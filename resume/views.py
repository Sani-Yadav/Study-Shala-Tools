from django.http import HttpResponse
from django.template.loader import get_template
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
from django.shortcuts import render


def generate_pdf(request, resume_id):
    try:
        # Get the resume with all related data in a single query
        resume = Resume.objects.select_related('user').prefetch_related(
            'experiences', 'education_entries', 'projects',
            'certifications', 'achievements', 'references'
        ).get(id=resume_id)
        
        template_path = 'resume/simple_resume.html'
        
        # Process skills and languages into lists
        def process_skills(skills_str):
            if not skills_str:
                return []
            return [skill.strip() for skill in skills_str.split(',') if skill.strip()]
            
        # Prepare context with all resume data
        context = {
            'resume': resume,
            'profile_image_url': request.build_absolute_uri(resume.profile_image.url) if resume.profile_image else None,
            'technical_skills': process_skills(resume.technical_skills),
            'soft_skills': process_skills(resume.soft_skills),
            'languages': process_skills(resume.languages),
            'hobbies': process_skills(resume.hobbies),
        }

        # Render template
        template = get_template(template_path)
        html = template.render(context)

        # Create PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{resume.full_name}_resume.pdf"'

        # Generate PDF
        pisa_status = pisa.CreatePDF(
            html,
            dest=response,
            encoding='UTF-8',
            link_callback=None
        )

        if pisa_status.err:
            return HttpResponse('PDF generation failed. Please try again.')

        return response
        
    except Resume.DoesNotExist:
        return HttpResponse('Resume not found', status=404)
    except Exception as e:
        return HttpResponse(f'An error occurred: {str(e)}', status=500)

def upload_resume(request):
    return render(request, 'resume/upload_resume.html')


def builder(request):
    """
    View for the resume builder page
    """
    # If user is not authenticated, redirect to login
    if not request.user.is_authenticated:
        from django.shortcuts import redirect
        from django.urls import reverse
        return redirect(f"{reverse('accounts:login')}?next={reverse('resume:builder')}")
    
    # Get or create resume for the current user
    resume, created = Resume.objects.get_or_create(user=request.user)
    
    # Handle form submission
    if request.method == 'POST':
        # Update basic resume fields
        resume.full_name = request.POST.get('full_name', '')
        resume.email = request.POST.get('email', '')
        resume.phone = request.POST.get('phone', '')
        resume.location = request.POST.get('location', '')
        resume.linkedin = request.POST.get('linkedin', '')
        resume.github = request.POST.get('github', '')
        resume.portfolio_url = request.POST.get('portfolio_url', '')
        resume.summary = request.POST.get('summary', '')
        resume.technical_skills = request.POST.get('technical_skills', '')
        resume.soft_skills = request.POST.get('soft_skills', '')
        resume.languages = request.POST.get('languages', '')
        resume.hobbies = request.POST.get('hobbies', '')
        
        # Handle profile image upload
        if 'profile_image' in request.FILES:
            resume.profile_image = request.FILES['profile_image']
        
        # Save the resume first to get an ID for related models
        resume.save()
        
        # Handle Work Experience
        job_titles = request.POST.getlist('job_title[]')
        companies = request.POST.getlist('company[]')
        start_dates = request.POST.getlist('start_date[]')
        end_dates = request.POST.getlist('end_date[]')
        job_descriptions = request.POST.getlist('job_description[]')  # Changed from descriptions to job_descriptions
        
        # Clear existing experiences
        resume.experiences.all().delete()
        
        # Add new experiences
        for i in range(len(job_titles)):
            if job_titles[i] or companies[i]:
                Experience.objects.create(
                    resume=resume,
                    job_title=job_titles[i],
                    company=companies[i],
                    start_date=start_dates[i] if i < len(start_dates) else '',
                    end_date=end_dates[i] if i < len(end_dates) else '',
                    description=job_descriptions[i] if i < len(job_descriptions) else ''
                )
        
        # Handle Education
        degrees = request.POST.getlist('degree[]')
        institutions = request.POST.getlist('institution[]')
        edu_start_dates = request.POST.getlist('edu_start_date[]')
        edu_end_dates = request.POST.getlist('edu_end_date[]')
        edu_descriptions = request.POST.getlist('edu_description[]')
        
        # Clear existing education
        resume.education_entries.all().delete()
        
        # Add new education entries
        for i in range(len(degrees)):
            if degrees[i] or institutions[i]:
                Education.objects.create(
                    resume=resume,
                    degree=degrees[i],
                    institution=institutions[i],
                    start_date=edu_start_dates[i] if i < len(edu_start_dates) else '',
                    end_date=edu_end_dates[i] if i < len(edu_end_dates) else '',
                    description=edu_descriptions[i] if i < len(edu_descriptions) else ''
                )
        
        # Handle Projects
        project_titles = request.POST.getlist('project_title[]')
        project_descriptions = request.POST.getlist('project_description[]')
        tech_stacks = request.POST.getlist('tech_stack[]')
        project_links = request.POST.getlist('project_link[]', [])
        
        # Clear existing projects
        resume.projects.all().delete()
        
        # Add new projects
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
        
        # Redirect to prevent form resubmission
        from django.shortcuts import redirect
        return redirect('resume:builder')
    
    # Render the builder template with resume data
    return render(request, 'resume/builder.html', {'resume': resume})
