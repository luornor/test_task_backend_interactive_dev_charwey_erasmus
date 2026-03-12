from django.core.exceptions import ValidationError
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import requests
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from .services import register_user
from django.utils.crypto import get_random_string
from django.db import transaction

def validate_token(*,token:str):
    request = google_requests.Request()

    try:
        id_info = id_token.id_token.verify_oauth2_token(
            token,
            request,
            settings.GOOGLE_CLIENT_ID
        )

        if id_info['iss'] not in ['accounts.google.com','https://accounts.google.com']:
            raise ValidationError('Wrong issuer.')
    except Exception as e:
        raise AuthenticationFailed("Invalid Google Token.")
    return id_info

@transaction.atomic
def google_login(*,id_token:str):
    google_data = validate_token(token=id_token)

    email = google_data.get('email')
    if not email:
        raise AuthenticationFailed("Invalid Google Token.")

    try:
        user = User.objects.get(email=email)
        return user
    except User.DoesNotExist:
        first_name = google_data.get('given_name', '')
        last_name = google_data.get('family_name', '')


        user = register_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            source='google',
            password=get_random_string(32),
        )
        user.is_email_verified = True
        user.save()
        return user


def facebook_validate_token(*, access_token: str) -> dict:
    try:
        graph_url = "https://graph.facebook.com/v18.0/me"
        params = {
            "access_token": access_token,
            "fields": "id,name,email,first_name,last_name,picture.width(400)"
        }

        response = requests.get(graph_url, params=params)
        response.raise_for_status()
        return response.json()

    except requests.RequestException as e:
        raise AuthenticationFailed("Invalid Facebook Token.")


@transaction.atomic
def login_with_facebook(*, access_token: str) -> User:
    fb_data = facebook_validate_token(access_token=access_token)

    email = fb_data.get('email')
    if not email:
        raise AuthenticationFailed("Facebook account has no email visibility. Please register with email.")

    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        first_name = fb_data.get('first_name', '')
        last_name = fb_data.get('last_name', '')

        user = register_user(
            email=email,
            password=User.objects.make_random_password(),
            first_name=first_name,
            last_name=last_name,
        )
        user.is_email_verified = True
        user.save()
        return user

