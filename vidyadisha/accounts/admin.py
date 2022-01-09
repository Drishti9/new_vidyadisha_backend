from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(User)
admin.site.register(Student)
"""admin.site.register(Mentor)
admin.site.register(Tutor)
admin.site.register(Subject)
admin.site.register(Donor)"""