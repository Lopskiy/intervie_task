from celery import shared_task, states
from celery.exceptions import Ignore
from .models import House, WaterMeterReading, Tariff, MonthlyBill, CalculationProgress
from django.db import transaction
from decimal import Decimal
import logging

@shared_task(bind=True)
def calculate_rent(self, house_id, month, year):
    self.update_state(state='PROGRESS', meta={'house_id': house_id, 'month': month, 'year': year})

    try:
        house = House.objects.get(id=house_id)
        maintenance_tariff = house.tarif
        progress = CalculationProgress.objects.create(house=house, month=month, year=year)
    except (House.DoesNotExist, Tariff.DoesNotExist) as e:
        logging.error(f"Error fetching house or tariffs: {e}")
        self.update_state(state='FAILURE', meta={'exc_type': str(type(e)), 'exc_message': str(e)})
        raise Ignore()

    try:
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

        progress.status = 'COMPLETED'
        progress.result = f"Calculation completed for house {house.address} for {month}/{year} total_cost {total_rent}"
        progress.save()
        self.update_state(state='SUCCESS', meta={'house_id': house_id, 'month': month, 'year': year, 'result': progress.result})
        return progress.result
    except Exception as e:
        logging.error(f"Error during calculation: {e}")
        progress.status = 'FAILED'
        progress.result = str(e)
        progress.save()
        self.update_state(state='FAILURE', meta={'exc_type': str(type(e)), 'exc_message': str(e)})
        raise Ignore()
