from django.urls import path
from .views import *

urlpatterns = [
    path('users/', UserInfoView.as_view(), name='users'),
    path('users/<int:pk>/', UserInfoView.as_view(), name='user-detail'),
    path('users/delete/<int:pk>/', user_delete, name='user-delete'),
    path('users/add/', AddUser.as_view(), name='user-add'),
    path('staffs/', StaffInfoView.as_view(), name='staffs'),
    path('staffs/<int:pk>/', StaffInfoView.as_view(), name='staff-detail'),
    path('staffs/delete/<int:pk>/', staff_delete, name='staff-delete'),
    path('staffs/add/', AddStaff.as_view(), name='staff-add'),
    path('blogs/',  BlogView.as_view(), name='blogs'),
    path('blogs/<int:pk>/', BlogView, name='blog-detail'),
    path('blogs/delete/<int:pk>/', blog_delete, name='blog-delete'),
    path('blogs/add/', AddBlog.as_view(), name='blog-add'),
    path('problems/', ProblemView.as_view(), name='problems'),
    path('problems/<int:pk>/', ProblemView.as_view(), name='problem-detail'),
    path('problems/add/', AddProblem.as_view(), name='problem-add'),
    path('problems/delete/<int:pk>/', problem_delete, name='problem-delete'),

]