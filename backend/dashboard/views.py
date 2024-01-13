# from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

from .models import OrderHistory
from .serializers import OrderHistorySerializer, OrderHistorySerializerEntry
from rest_framework.views import APIView

# from django.http import JsonResponse

#  import Response, status
from rest_framework.response import Response
from rest_framework import status


class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            user_orders = OrderHistory.objects.filter(user_name=request.user)
            serializer = OrderHistorySerializer(user_orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format="json"):  # noqa: A002
        try:
            print(request.data)
            serializer = OrderHistorySerializerEntry(data=request.data)
            if serializer.is_valid():
                instance = OrderHistory.objects.create(
                    user_identifier=request.data["user_identifier"],
                    user_name=request.data["user_name"],
                    organization=request.data["organization"],
                    amount=request.data["amount"],
                )
                if instance:
                    return Response(status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
