from django.contrib import admin
from .models import Category, Product, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'price', 'available', 'is_clothing', 'stock', 'created', 'updated']
    list_filter = ['available', 'is_clothing', 'created', 'updated', 'category']
    list_editable = ['price', 'available', 'is_clothing', 'stock']
    prepopulated_fields = {'slug': ('name',)}

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    readonly_fields = ['size']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'first_name', 'last_name', 'email', 'paid', 'payment_status', 'created', 'updated']
    list_filter = ['paid', 'payment_status', 'created', 'updated']
    inlines = [OrderItemInline]
    readonly_fields = ['order_id']
