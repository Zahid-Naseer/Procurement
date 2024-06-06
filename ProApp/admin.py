from django.contrib import admin
from ProApp.models import Project, UserProfile , Employee , Role , UserEmployeeMapping
# Register your models here.

admin.site.register(Project)
admin.site.register(UserProfile)
admin.site.register(Employee)
admin.site.register(Role)
admin.site.register(UserEmployeeMapping)