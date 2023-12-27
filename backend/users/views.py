from django.db import transaction
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import send_normal_email

from .models import NewUser, UserProfile


from .models import UserProfile
from .serializers import (
    PasswordRestSerializer,
    NewUserSerializer,
    ResetPasswordSerializer,
)


class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format="json"):  # noqa: A002
        try:
            with transaction.atomic():
                serializer = NewUserSerializer(data=request.data)
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
        # TODO: here return whole user porfile and then select what you need on the front end
        #  this is how you can make this more general and usable
        return JsonResponse({"payment_type": user_profile.payment_type})


class PasswordRestRequestView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordRestSerializer

    # add mail serializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        try:
            if serializer.is_valid(raise_exception=True):
                email = serializer.data.get("email")
                user = NewUser.objects.filter(email=email).first()
                if user:
                    encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
                    token = PasswordResetTokenGenerator().make_token(user)
                    current_site = get_current_site(request).domain
                    relativeLink = reverse(
                        "users:reset-password",
                        kwargs={"encoded_pk": encoded_pk, "token": token},
                    )
                    if "127.0.0.1" in current_site:
                        absurl = f"http://{current_site}{relativeLink}"
                    else:
                        absurl = f"https://{current_site}{relativeLink}"
                    return JsonResponse(
                        {"message": f"Your password link url {absurl}"},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return JsonResponse(
                        {"message": "User does not exist"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
        except Exception as e:
            return JsonResponse(
                {"message": "something is wrong with your email"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ResetPasswordAPIView(generics.GenericAPIView):
    """
    Verify and Reset Password Token View.
    """

    serializer_class = ResetPasswordSerializer

    def patch(self, request, *args, **kwargs):
        """
        Verify token & encoded_pk and then reset the password.
        """
        serializer = self.serializer_class(
            data=request.data, context={"kwargs": kwargs}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            {"message": "Password reset complete"},
            status=status.HTTP_200_OK,
        )
