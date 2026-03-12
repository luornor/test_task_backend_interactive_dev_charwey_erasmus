from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager
from django.utils.translation import gettext_lazy as _
import uuid
# Create your models here.



class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class User(AbstractUser, BaseModel):
    email = models.EmailField(unique=True, null=True, blank=True)
    username = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        indexes = [
            models.Index(fields=['email', 'is_active']),
            models.Index(fields=['phone_number', 'is_active']),
        ]

        # Ensure at least one auth method is present
        constraints = [
            models.CheckConstraint(
                condition=models.Q(email__isnull=False) | models.Q(phone_number__isnull=False),
                name='users_user_email_or_phone_required'
            )
        ]

    def __str__(self):
        return self.email or self.phone_number


class Profile(BaseModel):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11, unique=True)
    avatar = models.ImageField(upload_to='profile_pics',default='profile_pics/default.png',blank=True)

    def __str__(self):
        return self.user.email or self.phone_number
