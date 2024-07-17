from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HouseViewSet, ApartmentViewSet, WaterMeterViewSet, WaterMeterReadingViewSet, TariffViewSet, MonthlyBillViewSet

router = DefaultRouter()
router.register(r'houses', HouseViewSet)
router.register(r'apartments', ApartmentViewSet)
router.register(r'water-meters', WaterMeterViewSet)
router.register(r'water-meter-readings', WaterMeterReadingViewSet)
router.register(r'tariffs', TariffViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('calculate_rent/<int:house_id>/<int:month>/<int:year>/', MonthlyBillViewSet.as_view(), name='calculate_rent'),
]