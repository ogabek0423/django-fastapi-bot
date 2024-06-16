from django.contrib import admin
from .models import Problem, UserInfo, Blog, StaffInfo

admin.site.register([Problem, UserInfo, Blog, StaffInfo])