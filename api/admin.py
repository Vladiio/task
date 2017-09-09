from django.contrib import admin

from .models import Task, CustomToken


admin.site.register(Task)
admin.site.register(CustomToken)