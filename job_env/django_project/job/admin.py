from django.contrib import admin
from .models import Job, ApplyJob, State, Industry

# Register your models here.
admin.site.register(State)
admin.site.register(Industry)