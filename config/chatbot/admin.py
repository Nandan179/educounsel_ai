from django.contrib import admin
from .models import University, Course, UniversityPolicy

admin.site.register(University)
admin.site.register(Course)
admin.site.register(UniversityPolicy)
