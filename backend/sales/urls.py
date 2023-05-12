from rest_framework import routers
from django.urls import path, include
from . import views

# router = routers.DefaultRouter()
# router.register(r'items', views.ItemViewSet)
# router.register(r'item-prices', views.ItemPriceViewSet)
# router.register(r'daily-sales', views.DailySaleViewSet)
# router.register(r'food-sales', views.FoodSaleViewSet)

# urlpatterns = router.urls

urlpatterns = [
    path(r'items/', views.ItemList.as_view()),
    path(r'items/<int:itemId>', views.ItemDetail.as_view()),
    path(r'item-prices/', views.ItemPriceList.as_view()),
    path(r'item-prices/<int:itemPriceId>', views.ItemPriceDetail.as_view()),
    path(r'daily-sales/', views.DailySaleList.as_view()),
    path(r'daily-sales/<int:dailySaleId>', views.DailySaleDetail.as_view()),
    path(r'food-sales/', views.FoodSaleList.as_view()),
    path(r'food-sales/<int:foodSaleId>', views.FoodSaleDetail.as_view()),
]
