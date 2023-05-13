from django.urls import path
from .views import *

urlpatterns = [
 
    path("items/", ItemListView.as_view(), name="item-list"),
    path("item/<int:pk>/", ItemDetailView.as_view(), name="item"),
    path("item/add", ItemCreateView.as_view(), name="item-add"),
    path("item/<int:pk>/update", ItemUpdateView.as_view(), name="item-update"),
    path("item/<int:pk>/delete", ItemDeleteView.as_view(), name="item-delete"),

    path("dailysales/", DailySaleListView.as_view(), name="dailysale-list"),
    path("dailysale/<int:pk>/", DailySaleDetailView.as_view(), name="dailysale"),
    # path("dailysale/add", DailySaleCreateView.as_view(), name="dailysale-add"),
    path("dailysale/add", daily_add, name="dailysale-add"),
    path("dailysale/<int:pk>/update", daily_update, name="dailysale-update"),
    path("dailysale/<int:pk>/delete", DailySaleDeleteView.as_view(), name="dailysale-delete"),

    path("foodsales/", FoodSaleListView.as_view(), name="foodsale-list"),
    path("foodsale/<int:pk>/", FoodSaleDetailView.as_view(), name="foodsale"),
    path("foodsale/add", FoodSaleCreateView.as_view(), name="foodsale-add"),
    path("foodsale/<int:pk>/update", FoodSaleUpdateView.as_view(), name="foodsale-update"),
    path("foodsale/<int:pk>/delete", FoodSaleDeleteView.as_view(), name="foodsale-delete"),

]
