from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Project)
admin.site.register(UserStory)
admin.site.register(Sprint)
admin.site.register(ProjectMember)
admin.site.register(AssignedRole)
admin.site.register(Task)
admin.site.register(TimeEntry)