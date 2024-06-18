from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import *
from .forms import *
from users.models import *


class ServiceView(LoginRequiredMixin, View):
    def get(self, request):
        products = Product.objects.all()
        blogs = Blog.objects.all()
        context = {
            'products': products,
            'blogs': blogs
        }
        return render(request, 'services.html', context)

class ProductView(LoginRequiredMixin, View):
    def get(self, request, pk=None):
        if pk:
            product = Product.objects.get(id=pk)
            form = ProductForm(instance=product)
            return render(request, 'product_detail.html', {'form': form, 'product': product})
        else:
            products = Product.objects.all()
            categories = Category.objects.all()
            return render(request, 'shop.html', {'products': products, 'categories': categories})

    def post(self, request, pk=None):
        product = None
        if pk:
            product = Product.objects.get(id=pk)
            form = ProductForm(request.POST, instance=product)
        elif product is None:
            form = ProductForm(request.POST)
        else:
            return redirect('shop')

        if form.is_valid():
            form.save()
            return redirect('shop')

        if pk:
            return render(request, 'product_detail.html', {'form': form, 'product': product})
        else:
            return render(request, 'product_form.html', {'form': form})

@login_required(login_url='login')
def product_delete(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return redirect('shop')

class AddProduct(LoginRequiredMixin, View):
    def get(self, request):
        form = ProductForm()
        return render(request, 'product_form.html', context={'form': form})

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shop')
        else:
            return render(request, 'product_form.html', status=status.HTTP_400_BAD_REQUEST)


class CouponView(LoginRequiredMixin, View):
    def get(self, request, pk=None):
        if pk:
            coupon = Coupon.objects.get(id=pk)
            form = CouponForm(instance=coupon)
            return render(request, 'coupon-detail.html', {'form': form, 'coupon': coupon})
        else:
            coupons = Coupon.objects.all()
            return render(request, 'coupons.html', {'coupons': coupons})

    def post(self, request, pk=None):
        coupon = None
        if pk:
            coupon = Coupon.objects.get(id=pk)
            form = CouponForm(request.POST, instance=coupon)
        elif coupon is None:
            form = CouponForm(request.POST)
        else:
            return redirect('coupons')

        if form.is_valid():
            form.save()
            return redirect('coupons')

        if pk:
            return render(request, 'coupons.html', {'form': form, 'product': product})
        else:
            return render(request, 'add-coupon.html', {'form': form})

@login_required(login_url='login')
def coupon_delete(request, pk):
    coupon = Coupon.objects.get(id=pk)
    coupon.delete()
    return redirect('coupons')


class AddCoupon(LoginRequiredMixin, View):
    def get(self, request):
        form = CouponForm()
        return render(request, 'add-coupon.html', context={'form': form})

    def post(self, request):
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('coupons')
        else:
            return render(request, 'add-coupon.html', status=status.HTTP_400_BAD_REQUEST)


class PaymentView(LoginRequiredMixin, View):
    def get(self, request, pk=None):
        if pk:
            pay = Payment.objects.get(id=pk)
            form = PaymentForm(instance=pay)
            return render(request, 'pay-detail.html', {'form': form, 'pay': pay})
        else:
            pays = Product.objects.all()
            return render(request, 'pays.html', {'pays': pays})

    def post(self, request, pk=None):
        pay = None
        if pk:
            pay = Payment.objects.get(id=pk)
            form = PaymentForm(request.POST, instance=pay)
        elif pay is None:
            form = PaymentForm(request.POST)
        else:
            return redirect('payments')

        if form.is_valid():
            form.save()
            return redirect('payments')

        if pk:
            return render(request, 'pay-detail.html', {'form': form, 'pay': pay})
        else:
            return render(request, 'pays.html', {'form': form})

@login_required(login_url='login')
def pay_delete(request, pk):
    pay = Payment.objects.get(id=pk)
    pay.delete()
    return redirect('payments')


class AddPay(LoginRequiredMixin, View):
    def get(self, request):
        form = PaymentForm()
        return render(request, 'add-pay.html', context={'form': form})

    def post(self, request):
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payments')
        else:
            return render(request, 'add-pay.html', status=status.HTTP_400_BAD_REQUEST)

class TelegramUsersView(LoginRequiredMixin, View):
    def get(self, request, pk=None):
        if pk:
            user = TelegramUser.objects.get(id=pk)
            form = TelegramForm(instance=user)
            return render(request, 'detail-tg.html', {'form': form, 'user': user})
        else:
            users = TelegramUser.objects.all()
            return render(request, 'tg.html', {'users': users})

    def post(self, request, pk=None):
        user = None
        if pk:
            user = TelegramUser.objects.get(id=pk)
            form = TelegramForm(request.POST, instance=user)
        elif pay is None:
            form = TelegramForm(request.POST)
        else:
            return redirect('telegramuser')

        if form.is_valid():
            form.save()
            return redirect('telegramuser')

        if pk:
            return render(request, 'detail-tg.html', {'form': form, 'user': user})
        else:
            return render(request, 'tg.html', {'form': form})

@login_required(login_url='login')
def user_delete(request, pk):
    user = TelegramUser.objects.get(id=pk)
    user.delete()
    return redirect('telegramuser')


class AddUser(LoginRequiredMixin, View):
    def get(self, request):
        form = TelegramForm()
        return render(request, 'add-tg.html', context={'form': form})

    def post(self, request):
        form = TelegramForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('telegramuser')
        else:
            return render(request, 'add-tg.html', status=status.HTTP_400_BAD_REQUEST)
