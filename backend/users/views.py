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
    UserProfileSerializer,
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


# TODO: refactor this to more idiomatic Django
# class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsAuthenticated]
#     queryset = UserProfile.objects.all()
#     serializer_class = UserProfileSerializer


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format="json"):  # noqa: A002
        try:
            user_profile = UserProfile.objects.get(user__user_name=request.user)
            serializer = UserProfileSerializer(user_profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)


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

                    data = {
                        "email_subject": "Password Reset Request",
                        "email_body": f"Hi {user.user_name},\nPlease use the link below to reset your password\n{absurl}",
                        "to_email": user.email,
                    }
                    # send email
                    send_normal_email(data)
                    return JsonResponse(
                        {
                            "message": f"Your password link aws sent on email! Here it is url {absurl}"
                        },
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
