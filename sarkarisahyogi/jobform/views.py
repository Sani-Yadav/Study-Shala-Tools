from django.shortcuts import render, redirect
from .forms import UserProfileForm, JobApplicationForm
from .models import UserProfile, JobApplication
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect('sarkarisahyogi:apply_job')  # Added namespace
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'jobform/profile.html', {'form': form})

@login_required
def apply_job(request):
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            JobApplication.objects.create(
                user=request.user,
                job_title=form.cleaned_data['job_title']
            )
            return redirect('sarkarisahyogi:dashboard')  # Added namespace
    else:
        initial_data = {'job_title': 'Apply for Government Job'}
        form = JobApplicationForm(initial=initial_data)

    return render(request, 'jobform/apply_job.html', {'form': form, 'profile': profile})

@login_required
def dashboard(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return redirect('sarkarisahyogi:profile')  # Added namespace
        
    applications = JobApplication.objects.filter(user=request.user).order_by('-applied_on')
    
    context = {
        'profile': profile,
        'applications': applications,
        'total_applications': applications.count(),
        'approved_applications': applications.filter(status='Approved').count(),
        'pending_applications': applications.filter(status='Pending').count(),
        'rejected_applications': applications.filter(status='Rejected').count(),
    }
    
    return render(request, 'jobform/dashboard.html', context)
