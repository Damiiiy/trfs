from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(AdminUser)
admin.site.register(Exam)
# admin.site.register(Subject)
admin.site.register(Question)