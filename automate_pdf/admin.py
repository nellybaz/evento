from django.contrib import admin
from .models import Jobs


class JobsAdmin(admin.ModelAdmin):
    list_display = ('invite_file', 'invitees')
    fields = ('invite_file', 'invitees')




admin.site.register(Jobs, JobsAdmin)