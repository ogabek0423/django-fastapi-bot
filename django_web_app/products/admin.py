from django.contrib import admin
from .models import Payment, Product, Category, Coupon, TelegramUser
from import_export.admin import ImportExportModelAdmin


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ['name']
    list_display_links = ['name']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ['name', 'price', 'count']
    list_display_links = ['name', 'price', 'count']
    search_fields = ['name']


@admin.register(Coupon)
class CouponAdmin(ImportExportModelAdmin):
    list_display = ['code', 'value']
    list_display_links = ['code', 'value' ]
    search_fields = ['code', 'value']


@admin.register(Payment)
class PaymentAdmin(ImportExportModelAdmin):
    list_display = ['user', 'amount', 'pay_type']
    list_display_links = ['user', 'amount', 'pay_type']
    search_fields = ['user', 'amount', 'pay_type', 'coupon']


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'fullname', 'chat_id']
    list_display_links = ['username', 'fullname', 'chat_id']
    search_fields = ['username', 'chat_id']

