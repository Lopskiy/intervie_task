from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from celery.result import AsyncResult
from .models import House, Apartment, WaterMeter, WaterMeterReading, Tariff, CalculationProgress
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
        task = calculate_rent.delay(house_id, month, year)
        return Response({"task_id": task.id, "status": "Calculation started"}, status=status.HTTP_202_ACCEPTED)

class CalculationProgressView(APIView):
    def get(self, request, task_id):
        result = AsyncResult(task_id)
        if result.state == 'PENDING':
            return Response({"status": "PENDING"}, status=status.HTTP_200_OK)
        elif result.state == 'FAILURE':
            return Response({"status": "FAILED", "result": str(result.info)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            info = result.info
            if isinstance(info, dict):
                house_id = info.get('house_id')
                month = info.get('month')
                year = info.get('year')

                if house_id is not None and month is not None and year is not None:
                    progress_records = CalculationProgress.objects.filter(house_id=house_id, month=month, year=year)
                    if progress_records.exists():
                        progress = progress_records.first()
                        return Response({"status": progress.status, "result": progress.result}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status": "UNKNOWN"}, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({"status": "UNKNOWN"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"status": "UNKNOWN"}, status=status.HTTP_404_NOT_FOUND)