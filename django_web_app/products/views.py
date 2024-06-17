from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import *
from .forms import *


class ProductView(View):
    def get(self, request, pk=None):
        if pk:
            product = Product.objects.get(id=pk)
            form = ProductForm(instance=product)
            return render(request, 'product_detail.html', {'form': form, 'product': product})
        else:
            products = Product.objects.all()
            categories = Category.objects.all()
            return render(request, 'product_list.html', {'products': products, 'categories': categories})

    def post(self, request, pk=None):
        product = None
        if pk:
            product = Product.objects.get(id=pk)
            form = ProductForm(request.POST, instance=product)
        elif product is None:
            form = ProductForm(request.POST)
        else:
            return redirect('product_list')

        if form.is_valid():
            form.save()
            return redirect('product_list')

        if pk:
            return render(request, 'product_detail.html', {'form': form, 'product': product})
        else:
            return render(request, 'product_form.html', {'form': form})

# @login_required(login_url='login')
def product_delete(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return redirect('product_list')

class AddProduct(View):
    def get(self, request):
        form = ProductForm()
        return render(request, 'product_form.html', context={'form': form})

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
        else:
            return render(request, 'product_form.html', status=status.HTTP_400_BAD_REQUEST)


class CouponView(View):
    def get(self, request, pk=None):
        if pk:
            coupon = Coupon.objects.get(id=pk)
            form = CouponForm(instance=coupon)
            return render(request, '.html', {'form': form, 'coupon': coupon})
        else:
            coupons = Coupon.objects.all()
            return render(request, '.html', {'coupons': coupons})

    def post(self, request, pk=None):
        coupon = None
        if pk:
            coupon = Coupon.objects.get(id=pk)
            form = CouponForm(request.POST, instance=coupon)
        elif pay is None:
            form = CouponForm(request.POST)
        else:
            return redirect('')

        if form.is_valid():
            form.save()
            return redirect('')

        if pk:
            return render(request, '.html', {'form': form, 'product': product})
        else:
            return render(request, '.html', {'form': form})


def coupon_delete(request, pk):
    coupon = Coupon.objects.get(id=pk)
    coupon.delete()
    return redirect('')


class AddCoupon(View):
    def get(self, request):
        form = CouponForm()
        return render(request, '.html', context={'form': form})

    def post(self, request):
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('')
        else:
            return render(request, '.html', status=status.HTTP_400_BAD_REQUEST)


class PaymentView(View):
    def get(self, request, pk=None):
        if pk:
            pay = Payment.objects.get(id=pk)
            form = PaymentForm(instance=pay)
            return render(request, '.html', {'form': form, 'pay': pay})
        else:
            pays = Product.objects.all()
            return render(request, '.html', {'pays': pays})

    def post(self, request, pk=None):
        pay = None
        if pk:
            pay = Payment.objects.get(id=pk)
            form = PaymentForm(request.POST, instance=pay)
        elif pay is None:
            form = PaymentForm(request.POST)
        else:
            return redirect('')

        if form.is_valid():
            form.save()
            return redirect('')

        if pk:
            return render(request, '.html', {'form': form, 'product': product})
        else:
            return render(request, '.html', {'form': form})


def pay_delete(request, pk):
    pay = Payment.objects.get(id=pk)
    pay.delete()
    return redirect('')


class AddPay(View):
    def get(self, request):
        form = PaymentForm()
        return render(request, '.html', context={'form': form})

    def post(self, request):
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('')
        else:
            return render(request, '.html', status=status.HTTP_400_BAD_REQUEST)

class TelegramUsersView(View):
    def get(self, request, pk=None):
        if pk:
            user = TelegramUser.objects.get(id=pk)
            form = TelegramForm(instance=user)
            return render(request, '.html', {'form': form, 'user': user})
        else:
            users = TelegramUser.objects.all()
            return render(request, '.html', {'users': users})

    def post(self, request, pk=None):
        user = None
        if pk:
            user = TelegramUser.objects.get(id=pk)
            form = TelegramForm(request.POST, instance=user)
        elif pay is None:
            form = TelegramForm(request.POST)
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
    user = TelegramUser.objects.get(id=pk)
    user.delete()
    return redirect('')


class AddUser(View):
    def get(self, request):
        form = TelegramForm()
        return render(request, '.html', context={'form': form})

    def post(self, request):
        form = TelegramForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('')
        else:
            return render(request, '.html', status=status.HTTP_400_BAD_REQUEST)
