from rest_framework import routers
from django.urls import path, include
from .views import *
from . import models

item_list = ItemViewSet.as_view({'get':'list', 'post':'create'})
item_detail = ItemViewSet.as_view({'get':'retrieve', 'post': 'update'})
item_delete = ItemViewSet.as_view({'post':'destroy'})

itemprice_list = ItemPriceViewSet.as_view({'get':'list', 'post':'create'})
itemprice_detail = ItemPriceViewSet.as_view({'get':'retrieve', 'post':'update'})
itemprice_delete = ItemPriceViewSet.as_view({'post':'destroy'})



urlpatterns = [
        path(r'items/', item_list, name='item-list'),
        path(r'items/<int:pk>/delete', item_delete, name='item-delete'),
        path(r'items/<int:pk>/', item_detail, name='item'),

        path(r'itemprices/', itemprice_list, name='itemprice-list'),
        path(r'itemprices/<int:pk>/delete', itemprice_delete, name='itemprice-delete'),
        path(r'itemprices/<int:pk>/', itemprice_detail, name='itemprice'),

]
