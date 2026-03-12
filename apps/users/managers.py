from django.contrib.auth.models import BaseUserManager
from django.utils.crypto import get_random_string
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class UserManager(BaseUserManager):
    def _create_user(self, email, first_name, last_name, password, username=None, phone_number=None, **extra_fields):
        if not email and not phone_number:
            raise ValueError('User must have an email address or phone number')

        if not first_name:
            raise ValueError('User must have a first name')
        if not last_name:
            raise ValueError('User must have a last name')
        if email:
            email = self.normalize_email(email)
            try:
                validate_email(email)
            except ValidationError:
                raise ValueError('You must provide a valid email address')

        if not username:
            base = (email.split("@")[0] if email else None) or (phone_number or "user")
            username = base
            while self.model.objects.filter(username=username).exists():
                username = f"{base}_{get_random_string(4).lower()}"

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number if phone_number else None,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, first_name, last_name, password, username=None, phone_number=None, **extra_fields):
        extra_fields.setdefault('is_staff',False)
        extra_fields.setdefault('is_superuser',False)
        extra_fields.setdefault('is_active',True)

        if not email:
            raise ValueError('User must have an email address')

        return self._create_user(email, first_name, last_name, password, username, phone_number, **extra_fields)

    def create_superuser(self, email, first_name, last_name, password, username=None, phone_number=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        if not username:
            raise ValueError('Superuser must have a username.')

        return self._create_user(email, first_name, last_name, password, username, phone_number, **extra_fields)
