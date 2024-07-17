from celery import shared_task
from .models import House, WaterMeterReading, Tariff, MonthlyBill
from django.db import transaction
from decimal import Decimal

import logging

@shared_task
def calculate_rent(house_id, month, year):
    try:
        house = House.objects.get(id=house_id)
        maintenance_tariff = house.tarif
    except (House.DoesNotExist, Tariff.DoesNotExist) as e:
        logging.error(f"Error fetching house or tariffs: {e}")
        return str(e)

    with transaction.atomic():
        for apartment in house.apartments.all():
            water_charge = Decimal('0.0')
            for meter in apartment.water_meters.all():
                try:
                    current_reading = meter.readings.filter(date__month=month, date__year=year).order_by('-date').last()
                    previous_month = month - 1
                    previous_year = year
                    if previous_month == 0:
                        previous_month = 12
                        previous_year -= 1
                    previous_reading = meter.readings.filter(date__month=previous_month, date__year=previous_year).order_by('-date').last()
                    
                    if previous_reading and current_reading:
                        usage = current_reading.value - previous_reading.value
                        water_tariff = meter.tarif
                        water_charge += usage * water_tariff.price_per_unit
                except WaterMeterReading.DoesNotExist:
                    logging.warning(f"No water meter reading for apartment {apartment.id} in {month}/{year}")
                    continue

            maintenance_charge = apartment.area * maintenance_tariff.price_per_unit
            total_rent = water_charge + maintenance_charge

            MonthlyBill.objects.update_or_create(
                apartment=apartment,
                date=f'{month}/{year}',
                defaults={
                    'water_cost': water_charge,
                    'maintenance_cost': maintenance_charge,
                    'total_cost': total_rent
                }
            )

    return f"Calculation completed for house {house.address} for {month}/{year} total_cost {total_rent}"
