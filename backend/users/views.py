from django.db import transaction
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import UserProfile
from .serializers import CustomUserSerializer


class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format="json"):  # noqa: A002
        try:
            with transaction.atomic():
                serializer = CustomUserSerializer(data=request.data)
                if serializer.is_valid():
                    user = serializer.save()
                    if user:
                        json = serializer.data
                        profile = UserProfile.objects.create(user=user)
                        profile.save()
                        return Response(json, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)


class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format="json"):  # noqa: A002
        user_profile = UserProfile.objects.get(user=request.user)
        return JsonResponse({"payment_type": user_profile.payment_type})
