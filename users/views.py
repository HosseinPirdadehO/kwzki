from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import PublicUserSerializer
from rest_framework.generics import UpdateAPIView
from django.contrib.auth.hashers import check_password
from .serializers import ChangePasswordSerializer, PublicUserSerializer
from .serializers import AdminUserSerializer, PublicUserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer

# Create your views here.


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "ثبت‌نام با موفقیت انجام شد."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


User = get_user_model()


User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user.is_admin:
            return AdminUserSerializer
        return PublicUserSerializer

    def get_queryset(self):
        if self.request.user.is_admin:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)


User = get_user_model()


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = PublicUserSerializer(request.user)
        return Response(serializer.data)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        if not check_password(serializer.validated_data['old_password'], user.password):
            return Response({"detail": "رمز قبلی اشتباه است"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({"detail": "رمز عبور با موفقیت تغییر یافت"}, status=status.HTTP_200_OK)


class UpdateMeView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PublicUserSerializer

    def get_object(self):
        return self.request.user


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
