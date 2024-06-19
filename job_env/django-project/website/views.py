from django.shortcuts import render, redirect
from django.contrib import messages
from job.models import Job, ApplyJob
from .filter import JobFilter

# Create your views here.
def home(request):
    filter = JobFilter(request.GET, queryset=Job.objects.filter(is_available=True).order_by('-timestamp'))
    context = {
        'filter': filter
    }
    return render(request, 'website/home.html', context)

def job_listing(request):
    jobs = Job.objects.filter(is_available=True).order_by('-timestamp')
    context = {
        'jobs': jobs
    }
    return render(request, 'website/job_listing.html', context)

def job_details(request, pk):
    if request.user.is_authenticated:
        if ApplyJob.objects.filter(user=request.user, job_id=pk).exists():
            has_applied = True
        else:
            has_applied = False
    job = Job.objects.get(id=pk)
    has_applied = False
    context = {
        'job': job,
        'has_applied': has_applied
    }
    return render(request, 'website/job_details.html', context)
