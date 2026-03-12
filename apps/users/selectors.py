from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from .models import User


def get_user(*, user_id: str) -> User:
    return get_object_or_404(User, user_id=user_id)



def user_list(*, filters: dict = None) -> QuerySet[User]:
    filters = filters or {}
    qs = User.objects.select_related('profile').all().order_by('-created_at')

    if filters.get('role'):
        qs = qs.filter(groups__name=filters['role'])

    if filters.get('is_active') is not None:
        qs = qs.filter(is_active=filters['is_active'])

    if filters.get('is_verified_email') is not None:
        qs = qs.filter(is_verified_email=filters['is_verified_email'])


    if filters.get('is_verified_phone_number') is not None:
        qs = qs.filter(is_verified_phone_number=filters['is_verified_phone_number'])


    return qs
