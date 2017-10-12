from django.contrib import admin

# Register your models here.
from django.contrib import admin
from core.models import Repository

admin.site.register(Repository)
