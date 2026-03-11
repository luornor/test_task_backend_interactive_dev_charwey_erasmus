from typing import Optional

from django.db import transaction

from .models import User
from .utils import validate_phone_number
from django.core.exceptions import ValidationError
from .models import User
import logging

logger = logging.getLogger(__name__)

@transaction.atomic
def register_user(
        *,
        password: str,
        first_name: str,
        last_name: str,
        email: str = None,
        phone_number: str = None,
        source: str = None
) -> User:
    if not email and not phone_number:
        logger.error(f"Provide either 'email' or 'phone_number'.")
        raise ValidationError("Either email or phone number is required.")

    if phone_number:
        phone_number = validate_phone_number(phone_number)

    if email and User.objects.filter(email=email).exists():
        raise ValidationError({"email": "User with this email already exists."})
    if phone_number and User.objects.filter(phone_number=phone_number).exists():
        raise ValidationError({"phone_number": "User with this phone number already exists."})

    if source == "google":
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_active=True
        )
        print("source was google")

    else:
        user = User.objects.create_user(
            email=email,
            phone_number=phone_number if phone_number else None,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_active=True
        )

    return user
