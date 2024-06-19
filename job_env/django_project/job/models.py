from django.db import models
from users.models import User
from company.models import Company
from resume.models import Resume


# Create your models here.

class State(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Industry(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Job(models.Model):
    job_choices = (
        ('Remote', 'Remote'),
        ('Onsite', 'Onsite'),
        ('Hybrid', 'Hybrid'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    salary = models.PositiveIntegerField()
    requirements = models.TextField()
    ideal_candidate = models.TextField()
    is_available = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    industry = models.ForeignKey(Industry, on_delete=models.DO_NOTHING, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.DO_NOTHING, null=True, blank=True)
    job_type = models.CharField(max_length=255, choices=job_choices, null=True, blank=True)

    def __str__(self):
        return self.title
    
class ApplyJob(models.Model):
    status_choices = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),   
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, choices=status_choices, default='pending')
