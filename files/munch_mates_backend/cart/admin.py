from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('added_at', 'updated_at', 'total_price')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_id', 'created_at', 'updated_at', 'get_total_items')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'session_id')
    inlines = [CartItemInline]
    readonly_fields = ('created_at', 'updated_at')

    def get_total_items(self, obj):
        return sum(item.quantity for item in obj.items.all())
    get_total_items.short_description = 'Total Items'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'meal', 'quantity', 'total_price', 'added_at')
    list_filter = ('added_at', 'updated_at')
    search_fields = ('cart__user__username', 'cart__session_id', 'meal__name')
    readonly_fields = ('added_at', 'updated_at', 'total_price')
