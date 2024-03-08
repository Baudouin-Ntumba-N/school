
from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Grade)
admin.site.register(Option)
admin.site.register(Student, StudentAdmin)
admin.site.register(Prof, ProfAdmin)
admin.site.register(Course, CourseAdmin)