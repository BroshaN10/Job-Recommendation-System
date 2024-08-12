# Create your views here.
# jobs/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Job, UserProfile
from .recommendation import get_recommendations

def job_list(request):
    jobs = Job.objects.all().order_by('-posted_date')[:50]  # Get the latest 50 jobs
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

@login_required
def user_preferences(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        profile.preferences = request.POST.get('preferences', '')
        profile.save()
        return redirect('recommendations')
    return render(request, 'jobs/preferences_form.html', {'preferences': profile.preferences})

@login_required
def recommendations(request):
    profile = UserProfile.objects.get(user=request.user)
    recommended_jobs = get_recommendations(profile.preferences)
    return render(request, 'jobs/recommendations.html', {'jobs': recommended_jobs})