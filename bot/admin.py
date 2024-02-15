from django.contrib import admin

# Register your models here.

from .models import Discussion, Message


admin.site.register(Discussion)
admin.site.register(Message)