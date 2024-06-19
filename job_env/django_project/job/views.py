from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Job, ApplyJob
from .form import CreateJobForm, UpdateJobForm

# Create your views here.
def create_job(request):
    if request.user.is_recruiter and request.user.has_company:
        if request.method == 'POST':
            form = CreateJobForm(request.POST)
            if form.is_valid():
                var = form.save(commit=False)
                var.user = request.user
                var.company = request.user.company
                var.save()
                messages.info(request, 'New job has been created successfully.')
                return redirect('dashboard')
            else:
                messages.warning(request, 'Something went wrong')
        else:
            form = CreateJobForm()
            context = {
                'form': form
            }
        return render(request, 'job/create_job.html', context)
    else:
        messages.warning(request, 'You are not authorized to access this page')
        return redirect('dashboard')
    
def update_job(request, pk):
    if request.user.is_recruiter and request.user.has_company:
        job = Job.objects.get(id=pk)
        if request.method == 'POST':
            form = UpdateJobForm(request.POST, instance=job)
            if form.is_valid():
                form.save()
                messages.info(request, 'Job info has been updated successfully.')
                return redirect('dashboard')
            else:
                messages.warning(request, 'Something went wrong')
        else:
            form = UpdateJobForm(instance=job)
            context = {
                'form': form
            }
        return render(request, 'job/update_job.html', context)
    else:
        messages.warning(request, 'You are not authorized to access this page')
        return redirect('dashboard')
    
def manage_job(request):
    jobs = Job.objects.filter(user=request.user,company=request.user.company)
    context = {
        'jobs': jobs
    }
    return render(request, 'job/manage_job.html', context)

def apply_job(request, pk):
    if request.user.is_authenticated and request.user.is_applicant:
        job = Job.objects.get(id=pk)
        if ApplyJob.objects.filter(user=request.user, job=pk).exists():
            messages.warning(request, 'You have already applied for this job')
            return redirect('dashboard')
        else:
            ApplyJob.objects.create(
                user=request.user,
                job=job
                )
            messages.info(request, 'you have applied for this job successfully! Please see your dashboard for more info.')
            return redirect('dashboard')
    else:
        messages.warning(request, 'Please login to continue')
        return redirect('login')
        
def all_applicants(request, pk):
    job = Job.objects.get(id=pk)
    applicants = job.applyjob_set.all()
    context = {
        'job': job,
        'applicants': applicants
    }
    return render(request, 'job/all_applicants.html', context)

def applied_jobs(request):
    jobs = Job.objects.filter(applyjob__user=request.user)
    context = {
        'jobs': jobs
    }
    return render(request, 'job/applied_jobs.html', context)