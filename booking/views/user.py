from django.contrib.auth import authenticate
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status


from booking.models import User
from booking.serializers.user import RegisterUserSerializer
from booking.utils.set_jwt_cookie import set_jwt_cookies


class RegisterUserAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        response = Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )

        set_jwt_cookies(response, user)

        return response


class LogInAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(
            request=request,
            email=email,
            password=password
        )

        if user:
            response = Response(
                status=status.HTTP_200_OK
            )

            set_jwt_cookies(response=response, user=user)

            return response

        else:
            return Response(
                data={"message": "Invalid email or password."},
                status=status.HTTP_401_UNAUTHORIZED
            )


class LogOutAPIView(APIView):
    def post(self, request):
        response = Response(status=status.HTTP_200_OK)

        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response