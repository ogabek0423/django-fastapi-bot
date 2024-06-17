from django import forms
from .models import *


class UserForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['user', 'your_photo', 'city', 'street', 'home_number', 'user_number']

    def save(self, commit=True):
        user = super().save(commit)
        user.save()
        return user


class StaffForm(forms.ModelForm):
    class Meta:
        model = StaffInfo
        fields = ['user', 'photo', 'work_time', 'phone', 'experience']

    def save(self, commit=True):
        staff = super().save(commit)
        staff.save()
        return staff


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['text', 'user']

    def save(self, commit=True):
        data = super().save(commit)
        data.save()
        return data


class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['problem_text', 'user_email']

    def save(self, commit=True):
        data = super().save(commit)
        data.save()
        return data