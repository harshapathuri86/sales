from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'items', ItemViewSet)
router.register(r'item-prices', ItemPriceViewSet)
router.register(r'daily-sales', DailySaleViewSet)
router.register(r'food-sales', FoodSaleViewSet)

urlpatterns = router.urls
