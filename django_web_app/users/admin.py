from django.contrib import admin
from .models import Problem, UserInfo, Blog, StaffInfo
from import_export.admin import ImportExportModelAdmin


@admin.register(Problem)
class ProblemAdmin(ImportExportModelAdmin):
    list_display = ['user_email', 'slug']
    list_display_links = ['user_email', 'slug']
    search_fields = ['user_email', 'slug', 'problem_text']


@admin.register(UserInfo)
class UserInfoAdmin(ImportExportModelAdmin):
    list_display = ['user', 'user_number', 'home_number']
    list_display_links = ['user', 'user_number', 'home_number']
    search_fields = ['user', 'user_number', 'home_number']


@admin.register(StaffInfo)
class StaffInfoAdmin(ImportExportModelAdmin):
    list_display = ['user', 'phone', 'experience']
    list_display_links = ['user', 'phone', 'experience']
    search_fields = ['user', 'phone', 'experience']


@admin.register(Blog)
class BlogAdmin(ImportExportModelAdmin):
    list_display = ['user', 'slug']
    list_display_links = ['user', 'slug']
    search_fields = ['user', 'slug', 'text']

