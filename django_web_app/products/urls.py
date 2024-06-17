from django.urls import path
from .views import *

urlpatterns = [
    path('products/', ProductView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductView.as_view(), name='product_detail'),
    path('products/delete/<int:pk>/', product_delete, name='delete'),
    path('products/add/', AddProduct.as_view(), name='add_product'),
    path('coupons/', CouponView.as_view(), name='coupons'),
    path('coupons/<int:pk>/', CouponView.as_view(), name='coupon-detail'),
    path('coupons/delete/<int:pk>/', coupon_delete, name='delete-coupon'),
    path('coupons/add/', AddCoupon.as_view(), name='add_coupon'),
    path('payments/', PaymentView.as_view(), name='payments'),
    path('payments/<int:pk>/', PaymentView.as_view(), name='payment-detail'),
    path('payments/delete/<int:pk>/', pay_delete, name='delete-payment'),
    path('payments/add/', AddPay.as_view(), name='add_payment'),
    path('telegramuser/', TelegramUsersView.as_view(), name='telegram_users'),
    path('telegramuser/<int:pk>/', TelegramUsersView.as_view(), name='telegram_user-detail'),
    path('telegramuser/delete/<int:pk>/', user_delete, name='delete-telegram_user'),
    path('telegramuser/add/', AddUser.as_view(), name='add_telegram_user'),
]
