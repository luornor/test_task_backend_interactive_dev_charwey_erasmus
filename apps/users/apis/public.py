from ..services import register_user
from ..social_service import google_login, login_with_facebook
from ..serializers import (
    RegisterSerializer,
    UserSerializer,
    SlidingTokenRequestSerializer,
    SlidingRefreshRequestSerializer,
    SlidingTokenResponseSerializer,
    SlidingRefreshResponseSerializer,
    GoogleLoginInputSerializer,
    FacebookLoginInputSerializer,
)
from rest_framework import views, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from rest_framework_simplejwt.views import TokenObtainSlidingView, TokenRefreshSlidingView


class RegisterUser(views.APIView):
    @extend_schema(
        tags=['Public -User'],
        summary="Register User",
        request=RegisterSerializer,
        responses=UserSerializer
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        user = register_user(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data.get('email'),
            phone_number=data.get('phone_number'),
            username=data.get('username'),
            password=data['password']

        )
        user.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class SlidingTokenLogin(TokenObtainSlidingView):
    serializer_class = SlidingTokenRequestSerializer

    @extend_schema(
        tags=["Public -User"],
        summary="Login with JWT",
        request=SlidingTokenRequestSerializer,
        responses={
            200: OpenApiResponse(
                response=SlidingTokenResponseSerializer,
                description="Login Successful",
                examples=[
                    OpenApiExample(
                        "Success Response",
                        value={
                            "token": "eyJ...",
                            "refresh": "eyJ...",
                        },
                    )
                ],
            )
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class SlidingTokenRefresh(TokenRefreshSlidingView):
    serializer_class = SlidingRefreshRequestSerializer

    @extend_schema(
        tags=["Public -User"],
        summary="Refresh Sliding Token",
        request=SlidingRefreshRequestSerializer,
        responses={
            200: OpenApiResponse(
                response=SlidingRefreshResponseSerializer,
                description="Token refreshed",
                examples=[
                    OpenApiExample(
                        "Success Response",
                        value={
                            "token": "eyJ...",
                        },
                    )
                ],
            )
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class GoogleLogin(views.APIView):
    @extend_schema(
        tags=["Public -User"],
        summary="Login with Google",
        request=GoogleLoginInputSerializer,
        responses=UserSerializer,
    )
    def post(self, request):
        serializer = GoogleLoginInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = google_login(id_token=serializer.validated_data["id_token"])
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


class FacebookLogin(views.APIView):
    @extend_schema(
        tags=["Public -User"],
        summary="Login with Facebook",
        request=FacebookLoginInputSerializer,
        responses=UserSerializer,
    )
    def post(self, request):
        serializer = FacebookLoginInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = login_with_facebook(access_token=serializer.validated_data["access_token"])
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
