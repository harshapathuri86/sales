from rest_framework import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter()
router.register(r'items', views.ItemViewSet)
router.register(r'item-prices', views.ItemPriceViewSet)
router.register(r'daily-sales', views.DailySaleViewSet)
router.register(r'food-sales', views.FoodSaleViewSet)
urlpatterns = router.urls
