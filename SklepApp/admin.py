from django.contrib import admin
from .models import Product, Order, OrderItem, Address

admin.site.register(Product)
admin.site.register(Address)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "full_name",
        "status",
        "payment_method",
        "total",
        "created_at",
    )
    list_filter = ("status", "payment_method", "created_at")
    list_editable = ("status",)
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)