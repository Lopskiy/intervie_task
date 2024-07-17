# core/management/commands/populate_data.py

import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from core.models import Tariff, House, Apartment, WaterMeter, WaterMeterReading

class Command(BaseCommand):
    help = 'Populate the database with initial data'

    def handle(self, *args, **kwargs):
        self.create_tariffs()
        self.stdout.write(self.style.SUCCESS('Successfully created tariffs'))
        
        self.create_houses_and_apartments()
        self.stdout.write(self.style.SUCCESS('Successfully created houses and apartments'))
        
        self.create_water_meters_and_readings()
        self.stdout.write(self.style.SUCCESS('Successfully created water meters and readings'))
        
        self.stdout.write(self.style.SUCCESS('Successfully populated the database'))

    def create_tariffs(self):
        tariffs = [
            {'name': 'Standard', 'price_per_unit': 50.00},
            {'name': 'Premium', 'price_per_unit': 75.00},
            {'name': 'Basic', 'price_per_unit': 40.00},
        ]
        for tariff_data in tariffs:
            Tariff.objects.create(**tariff_data)

    def create_houses_and_apartments(self):
        tariffs = Tariff.objects.all()
        houses = [
            {'address': '123 Main St', 'tarif': random.choice(tariffs)},
            {'address': '456 Elm St', 'tarif': random.choice(tariffs)},
        ]
        for house_data in houses:
            house = House.objects.create(**house_data)
            for i in range(1, 5):  # Create 4 apartments for each house
                Apartment.objects.create(
                    house=house,
                    number=f'Apt {i}',
                    area=random.uniform(50.0, 150.0)
                )

    def create_water_meters_and_readings(self):
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
                try:
                    WaterMeterReading.objects.create(
                        water_meter=water_meter,
                        date=current_date,
                        value=random.uniform(50.0, 150.0)
                    )
                except IntegrityError:
                    self.stdout.write(self.style.WARNING(f'Skipping duplicate entry for {water_meter} on {current_date}'))
                current_date += timedelta(days=30)  # Monthly readings
