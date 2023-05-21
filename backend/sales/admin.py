from django.contrib import admin
from .models import *

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Counter)
class CounterAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(FoodSale)
class FoodSaleAdmin(admin.ModelAdmin):
    list_display = ('date', 'item','counter', 'prepared_quantity', 'leftover_quantity','price', 'sale')
    search_fields = ('date', 'item__name', 'counter__name')
    list_filter = ('date', 'item__name', 'counter__name')
