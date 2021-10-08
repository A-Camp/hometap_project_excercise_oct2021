from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Home

# Register your models here.
admin.site.register(Home)
admin.site.unregister(Group)