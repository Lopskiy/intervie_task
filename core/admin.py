from django.contrib import admin
from .models import House, Apartment, WaterMeter, WaterMeterReading, Tariff, MonthlyBill

admin.site.register(House)
admin.site.register(Apartment)
admin.site.register(WaterMeter)
admin.site.register(WaterMeterReading)
admin.site.register(Tariff)
admin.site.register(MonthlyBill)
