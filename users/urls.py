from .views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UpdateMeView, ChangePasswordView, MeView, UserViewSet, RegisterView, register_view
from rest_framework.routers import DefaultRouter
from django.urls import path


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
urlpatterns = router.urls


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', MeView.as_view(), name='me'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('me/update/', UpdateMeView.as_view(), name='update-me'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('form-register/', register_view, name='form-register'),
]
