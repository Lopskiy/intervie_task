from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import House, Apartment, WaterMeter, WaterMeterReading, Tariff
from .serializers import HouseSerializer, ApartmentSerializer, WaterMeterSerializer, WaterMeterReadingSerializer, TariffSerializer
from .tasks import calculate_rent
from django.shortcuts import get_object_or_404


class HouseViewSet(viewsets.ModelViewSet):
    queryset = House.objects.all()
    serializer_class = HouseSerializer

class ApartmentViewSet(viewsets.ModelViewSet):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer

class WaterMeterViewSet(viewsets.ModelViewSet):
    queryset = WaterMeter.objects.all()
    serializer_class = WaterMeterSerializer

class WaterMeterReadingViewSet(viewsets.ModelViewSet):
    queryset = WaterMeterReading.objects.all()
    serializer_class = WaterMeterReadingSerializer

class TariffViewSet(viewsets.ModelViewSet):
    queryset = Tariff.objects.all()
    serializer_class = TariffSerializer

class MonthlyBillViewSet(APIView):
    def post(self, request, house_id, month, year):
        house = get_object_or_404(House, id=house_id)
        calculate_rent.delay(house_id, month, year)
        return Response({"status": "Calculation started"}, status=status.HTTP_202_ACCEPTED)