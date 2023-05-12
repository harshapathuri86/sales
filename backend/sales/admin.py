from django.contrib import admin
from .models import *

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(ItemPrice)
class ItemPriceAdmin(admin.ModelAdmin):
    list_display = ('item', 'price', 'created_at')
    list_filter = ('item__name', 'created_at')

@admin.register(DailySale)
class DailySaleAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_sales')
    search_fields = ('date',)
    list_filter = ('date',)
    readonly_fields = ('total_sales',)

@admin.register(FoodSale)
class FoodSaleAdmin(admin.ModelAdmin):
    list_display = ('date', 'item', 'prepared_quantity', 'leftover_quantity','price', 'sale')
    search_fields = ('date__date', 'item__name')
    list_filter = ('date__date', 'item__name')
    readonly_fields = ('sale','price')
