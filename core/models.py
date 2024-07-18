from django.db import models
from django.core.validators import MinValueValidator

class Tariff(models.Model):
    name = models.CharField(max_length=100)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class House(models.Model):
    address = models.CharField(max_length=255)
    tarif = models.ForeignKey(Tariff, related_name='maintnence', on_delete=models.CASCADE)

    def __str__(self):
        return self.address

class Apartment(models.Model):
    house = models.ForeignKey(House, related_name='apartments', on_delete=models.CASCADE)
    number = models.CharField(max_length=10)
    area = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.01)])

    def __str__(self):
        return f"{self.house.address} - Apt {self.number}"

class WaterMeter(models.Model):
    apartment = models.ForeignKey(Apartment, related_name='water_meters', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    tarif = models.ForeignKey(Tariff, related_name='tarif', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.apartment} - {self.name}"

class WaterMeterReading(models.Model):
    water_meter = models.ForeignKey(WaterMeter, related_name='readings', on_delete=models.CASCADE)
    date = models.DateField()
    value = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('water_meter', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.water_meter} - {self.date}"

class MonthlyBill(models.Model):
    apartment = models.ForeignKey(Apartment, related_name='bills', on_delete=models.CASCADE)
    date = models.CharField(max_length=20)
    water_cost = models.DecimalField(max_digits=10, decimal_places=2)
    maintenance_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.apartment} - {self.date}"

    class Meta:
        unique_together = ('apartment', 'date')
    
class CalculationProgress(models.Model):
    house = models.ForeignKey(House, related_name='calculation_progress', on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()
    status = models.CharField(max_length=20, default='PENDING')
    result = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.house.address} - {self.month}/{self.year} - {self.status}"