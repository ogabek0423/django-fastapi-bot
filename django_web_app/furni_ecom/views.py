from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from products.models import Product, Category, TelegramUser, Coupon, Payment
from users.models import UserInfo, StaffInfo, Blog, Problem

class FurniEcomView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        categories = Category.objects.all()
        telegram_user = TelegramUser.objects.all()
        coupons = Coupon.objects.all()
        payments = Payment.objects.all()
        blogs = Blog.objects.all()
        context = {
            'products': products,
            'categories': categories,
            'telegram_user': telegram_user,
            'coupons': coupons,
            'payments': payments,
            'blogs': blogs
        }

        return render(request, 'index.html', context=context)
