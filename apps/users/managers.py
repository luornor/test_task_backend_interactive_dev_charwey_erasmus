from bench.exceptions import ValidationError
from django.contrib.auth.models import BaseUserManager
from django.core.validators import validate_email

class UserManager(BaseUserManager):
    def _create_user(self,password,first_name,last_name,email=None,phone_number=None,**extra_fields):
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

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number if phone_number else None,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self,email,first_name,last_name,phone_number=None,**extra_fields):
        extra_fields.setdefault('is_staff',False)
        extra_fields.setdefault('is_superuser',False)
        extra_fields.setdefault('is_active',True)

        if not email:
            raise ValueError('User must have an email address')

        return self._create_user(email,first_name,last_name,phone_number,**extra_fields)