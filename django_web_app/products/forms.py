from django import forms
from .models import *


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'count', 'endurance']

    def save(self, commit=True):
        product = super().save(commit)
        product.save()
        return product


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['user', 'product_list', 'amount', 'pay_type', 'coupon']

    def save(self, commit=True):
        pay = super().save(commit)
        pay.save()
        return pay


class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'value']

    def save(self, commit=True):
        coupon = super().save(commit)
        coupon.save()
        return coupon


class TelegramForm(forms.ModelForm):
    class Meta:
        model = TelegramUser
        fields = ['username', 'fullname', 'chat_id']

    def save(self, commit=True):
        user = super().save(commit)
        user.save()
        return user