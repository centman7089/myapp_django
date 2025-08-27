from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    UserRegisterSerializer,
    LoginSerializer,
    VerifyEmailSerializer
)
from .utils import send_code_to_user
from .models import OneTimePassword


class RegisterUserView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()  # create user
            # send OTP for verification
            send_code_to_user(user.email)

            return Response(
                {
                    "data": serializer.data,
                    "message": f"Hi {user.first_name}, thanks for signing up! "
                               f"A passcode has been sent to your email."
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyUserEmail(GenericAPIView):
    serializer_class = VerifyEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp_code = serializer.validated_data["otp"]

        try:
            user_code_obj = OneTimePassword.objects.get(code=otp_code)
            user = user_code_obj.user

            if not user.is_verified:
                user.is_verified = True
                user.save()

                # remove OTP after successful verification
                user_code_obj.delete()

                return Response(
                    {"message": "Account email verified successfully"},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"message": "User already verified"},
                    status=status.HTTP_200_OK
                )

        except OneTimePassword.DoesNotExist:
            return Response(
                {"message": "Passcode not found or expired"},
                status=status.HTTP_404_NOT_FOUND
            )


class LoginUserView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        return Response(
            {
                "message": "Login successful",
                "data": serializer.validated_data
            },
            status=status.HTTP_200_OK
        )


# 🔒 Protected endpoint (requires login)
class TestAuthenticationView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response(
            {"message": f"Hello {request.user.get_full_name}, you are authenticated!"},
            status=status.HTTP_200_OK
        )
