# django
from django.contrib import admin
# local
from .models import Order, OrderItem, Coupon
# Third-party


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = (
        'subscription',
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'updated',
        'paid'
    )
    list_filter = (
        'paid',
    )
    inlines = (OrderItemInline,)


admin.site.register(Coupon)
