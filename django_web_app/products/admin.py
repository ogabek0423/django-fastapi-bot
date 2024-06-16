from django.contrib import admin
from .models import Payment, Product, Category, Coupon, TelegramUser

admin.site.register([Payment, Product, Category, Coupon, TelegramUser])