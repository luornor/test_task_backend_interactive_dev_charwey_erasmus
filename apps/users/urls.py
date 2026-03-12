from django.urls import path
from apps.users.apis.public import (
    RegisterUser,
    SlidingTokenLogin,
    SlidingTokenRefresh,
    GoogleLogin,
    FacebookLogin,
)

urlpatterns = [
    path('token/', SlidingTokenLogin.as_view(), name='login'),
    path('token/refresh/', SlidingTokenRefresh.as_view(), name='token_refresh'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/google/', GoogleLogin.as_view(), name='google_login'),
    path('login/facebook/', FacebookLogin.as_view(), name='facebook_login'),
]
