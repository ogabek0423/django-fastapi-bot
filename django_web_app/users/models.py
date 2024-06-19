from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    your_photo = models.ImageField(upload_to='user_photos/')
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    home_number = models.CharField(max_length=50)
    user_number = models.CharField(max_length=20)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_info'
        ordering = ['id']
        indexes = [models.Index(fields=['id'])]

    def __str__(self):
        return self.user.first_name


class StaffInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='staff_photos/')
    work_time = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    experience = models.TextField()
    slug = models.SlugField(max_length=150, unique=True)

    class Meta:
        db_table = 'staff_info'
        ordering = ['id']
        indexes = [models.Index(fields=['id'])]

    def __str__(self):
        return self.user.last_name


@receiver(pre_save, sender=StaffInfo)
def pre_save_category_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)


class Blog(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        db_table = 'blog'
        ordering = ['id']
        indexes = [models.Index(fields=['id'])]

    def __str__(self):
        return self.user.first_name


@receiver(pre_save, sender=Blog)
def pre_save_blog_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.text[:50])

class Problem(models.Model):
    problem_text = models.TextField()
    user_email = models.EmailField()
    created_time = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        db_table = 'problems'
        ordering = ['id']
        indexes = [models.Index(fields=['id'])]

    def __str__(self):
        return self.user_email


@receiver(pre_save, sender=Problem)
def pre_save_pro_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.text[:50])