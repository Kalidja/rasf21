import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_datetime
from .models import Order
from django.shortcuts import render


def base_page(request):
    return render(request, "base.html")

def files_list(request):
    files = Order.objects.all()
    return render(request, "files_list.html", {"files": files})

class UploadJSONAPIView(APIView):

    def get(self, request):
        return render(request, "upload.html")

    def post(self, request):
        file = request.FILES.get('file')

        if not file:
            return Response(
                {"error": "Файл не передан"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            data = json.load(file)
        except Exception:
            return Response(
                {"error": "Некорректный JSON"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not isinstance(data, list):
            return Response(
                {"error": "Ожидается список объектов"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            parsed_date = datetime.strptime(data["date"], "%Y-%m-%d_%H:%M")
        except ValueError:
            return Response({"error": "Невозможно преобразовать дату"}, status=400)

        Order.objects.create(
            name=data["name"],
            date=parsed_date
        )

        return Response(
            {"message": f"Загружено {created} записей"},
            status=status.HTTP_201_CREATED
        )
