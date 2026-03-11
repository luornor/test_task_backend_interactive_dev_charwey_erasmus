from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainSlidingView,
    TokenRefreshSlidingView,
)

urlpatterns = [
    path('api/token/', TokenObtainSlidingView.as_view(), name='token_obtain'),
    path('api/token/refresh/', TokenRefreshSlidingView.as_view(), name='token_refresh'),
]