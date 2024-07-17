import os
import django
import random
from datetime import datetime, timedelta
from decimal import Decimal
from core.models import Tariff, House, Apartment, WaterMeter, WaterMeterReading

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'intervie_task.settings')
django.setup()

# Function to create tariffs
def create_tariffs():
    tariffs = [
        {'name': 'Standard', 'price_per_unit': 50.00},
        {'name': 'Premium', 'price_per_unit': 75.00},
        {'name': 'Basic', 'price_per_unit': 40.00},
    ]
    for tariff_data in tariffs:
        Tariff.objects.create(**tariff_data)

# Function to create houses and apartments
def create_houses_and_apartments():
    houses = [
        {'address': '123 Main St'},
        {'address': '456 Elm St'},
    ]
    for house_data in houses:
        house = House.objects.create(**house_data)
        for i in range(1, 5):  # Create 4 apartments for each house
            Apartment.objects.create(
                house=house,
                number=f'Apt {i}',
                area=random.uniform(50.0, 150.0)
            )

# Function to create water meters and readings
def create_water_meters_and_readings():
    apartments = Apartment.objects.all()
    for apartment in apartments:
        WaterMeter.objects.create(
            apartment=apartment,
            name=f'Water Meter {apartment.number}',
            tarif=random.choice(Tariff.objects.all())
        )

    # Create readings for each water meter for the past 6 months
    today = datetime.now().date()
    for water_meter in WaterMeter.objects.all():
        start_date = today - timedelta(days=180)  # 6 months ago
        current_date = start_date
        while current_date <= today:
            WaterMeterReading.objects.create(
                water_meter=water_meter,
                date=current_date,
                value=random.uniform(50.0, 150.0)
            )
            current_date += timedelta(days=30)  # Monthly readings

if __name__ == '__main__':
    create_tariffs()
    create_houses_and_apartments()
    create_water_meters_and_readings()
    print("Data populated successfully!")
