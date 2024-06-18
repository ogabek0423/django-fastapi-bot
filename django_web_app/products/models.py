from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class TelegramUser(models.Model):
    username = models.CharField(max_length=150, null=True)
    fullname = models.CharField(max_length=150)
    chat_id = models.BigIntegerField()
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'telegram_users'
        ordering = ['id']
        indexes = [models.Index(fields=['id'])]

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=100)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'category'
        ordering = ['id']
        indexes = [models.Index(fields=['id'])]

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    endurance = models.IntegerField()

    class Meta:
        db_table = 'products'
        ordering = ['id']
        indexes = [models.Index(fields=['id'])]

    def __str__(self):
        return self.name


class Coupon(models.Model):
    code = models.CharField(max_length=50)
    value = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'coupons'
        ordering = ['id']
        indexes = [models.Index(fields=['id'])]

    def __str__(self):
        return self.code


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_list = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    pay_type = models.CharField(max_length=50)
    pay_time = models.DateTimeField(auto_now_add=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'payments'
        ordering = ['id']
        indexes = [models.Index(fields=['id'])]

    def __str__(self):
        return self.user.first_name
