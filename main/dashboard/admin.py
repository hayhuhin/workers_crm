from django.contrib import admin

# Register your models here.

from dashboard.models import Employer,Job_position,Personal_task,Position_responsabilities,Lead_Creator

admin.site.register(Employer)
admin.site.register(Job_position)
admin.site.register(Personal_task)
admin.site.register(Position_responsabilities)
admin.site.register(Lead_Creator)