from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.contrib.auth.forms import AuthenticationForm


class UserLoginView(View):
    def get(self, request):
        form = UserLoginForm()
        context = {'form': form}
        return render(request, 'login.html', context)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        data = {
            "username": username,
            "password": password
        }
        login_form = AuthenticationForm(data=data)

        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect("index")
        else:

            context = {
                "form": login_form,
            }
            return render(request, "login.html", context)


class UserRegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        context = {'form': form}
        return render(request, 'register.html', context)


    def post(self, request):
        create_form = UserRegisterForm(data=request.POST)
        if create_form.is_valid():
            create_form.save()
            return redirect('login')

        else:
            context = {'form': create_form}
            return render(request, 'register.html', context)


class LogOutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')


class MyProfileView(View):
    def get(self, request):
        user = User.objects.get(username=request.user.username)

        context = {
                'user': user,
            }
        return render(request, 'my-profile.html', context)

    def post(self, request, pk=None):
        m_user = None
        if pk:
            m_user = User.objects.get(id=pk)
            form = UserRegisterForm(request.POST, instance=m_user)
        elif user is None:
            form = UserRegisterForm(request.POST)
        else:
            return redirect('')

        if form.is_valid():
            form.save()
            return redirect('')

        if pk:
            return render(request, '.html', {'form': form, 'user': m_user})
        else:
            return render(request, '.html', {'form': form})

def profile_delete(request, pk):
    user = User.objects.get(id=pk)
    user.delete()
    return redirect('index')


class UserInfoView(View):
    def get(self, request, pk=None):
        if pk:
            user = UserInfo.objects.get(id=pk)
            form = UserForm(instance=user)
            return render(request, '.html', {'form': form, 'user': user})
        else:
            users = UserInfo.objects.all()
            return render(request, '.html', {'users': users})

    def post(self, request, pk=None):
        user = None
        if pk:
            user = UserInfo.objects.get(id=pk)
            form = UserInfo(request.POST, instance=user)
        elif user is None:
            form = UserForm(request.POST)
        else:
            return redirect('')

        if form.is_valid():
            form.save()
            return redirect('')

        if pk:
            return render(request, '.html', {'form': form, 'user': user})
        else:
            return render(request, '.html', {'form': form})


def user_delete(request, pk):
    user = UserInfo.objects.get(id=pk)
    user.delete()
    return redirect('')


class AddUser(View):
    def get(self, request):
        form = UserForm()
        return render(request, '.html', context={'form': form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('')
        else:
            return render(request, '.html', status=status.HTTP_400_BAD_REQUEST)


class StaffInfoView(View):
    def get(self, request, pk=None):
        if pk:
            staff = StaffInfo.objects.get(id=pk)
            form = StaffForm(instance=staff)
            return render(request, '.html', {'form': form, 'staff': staff})
        else:
            staffs = StaffInfo.objects.all()
            return render(request, '.html', {'staffs': staffs})

    def post(self, request, pk=None):
        staff = None
        if pk:
            staff = StaffInfo.objects.get(id=pk)
            form = StaffForm(request.POST, instance=staff)
        elif staff is None:
            form = StaffForm(request.POST)
        else:
            return redirect('')

        if form.is_valid():
            form.save()
            return redirect('')

        if pk:
            return render(request, '.html', {'form': form, 'user': user})
        else:
            return render(request, '.html', {'form': form})


def staff_delete(request, pk):
    staff = StaffInfo.objects.get(id=pk)
    staff.delete()
    return redirect('')


class AddStaff(View):
    def get(self, request):
        form = StaffForm()
        return render(request, '.html', context={'form': form})

    def post(self, request):
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('')
        else:
            return render(request, '.html', status=status.HTTP_400_BAD_REQUEST)


class BlogView(View):
    def get(self, request, pk=None):
        if pk:
            blog = Blog.objects.get(id=pk)
            form = BlogForm(instance=blog)
            return render(request, '.html', {'form': form, 'blog': blog})
        else:
            blogs = Blog.objects.all()
            return render(request, '.html', {'blogs': blogs})

    def post(self, request, pk=None):
        blog = None
        if pk:
            blog = Blog.objects.get(id=pk)
            form = BlogForm(request.POST, instance=blog)
        elif blog is None:
            form = BlogForm(request.POST)
        else:
            return redirect('')

        if form.is_valid():
            form.save()
            return redirect('')

        if pk:
            return render(request, '.html', {'form': form, 'blog': blog})
        else:
            return render(request, '.html', {'form': form})


def blog_delete(request, pk):
    blog = Blog.objects.get(id=pk)
    blog.delete()
    return redirect('')


class AddBlog(View):
    def get(self, request):
        form = BlogForm()
        return render(request, '.html', context={'form': form})

    def post(self, request):
        form = BlogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('')
        else:
            return render(request, '.html', status=status.HTTP_400_BAD_REQUEST)



class ProblemView(View):
    def get(self, request, pk=None):
        if pk:
            problem = Problem.objects.get(id=pk)
            form = ProblemForm(instance=blog)
            return render(request, '.html', {'form': form, 'problem': problem})
        else:
            problems = Problem.objects.all()
            return render(request, '.html', {'problems': problems})

    def post(self, request, pk=None):
        problem = None
        if pk:
            problem = Problem.objects.get(id=pk)
            form = ProblemForm(request.POST, instance=blog)
        elif problem is None:
            form = ProblemForm(request.POST)
        else:
            return redirect('')

        if form.is_valid():
            form.save()
            return redirect('')

        if pk:
            return render(request, '.html', {'form': form, 'problem': problem})
        else:
            return render(request, '.html', {'form': form})


def problem_delete(request, pk):
    problem = Problem.objects.get(id=pk)
    problem.delete()
    return redirect('')


class AddProblem(View):
    def get(self, request):
        form = ProblemForm()
        return render(request, '.html', context={'form': form})

    def post(self, request):
        form = ProblemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('')
        else:
            return render(request, '.html', status=status.HTTP_400_BAD_REQUEST)

