from django.contrib import admin

# Register your models here.
from .models import User,Profile

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone_number')
    search_fields = ('email', 'phone_number')
    list_filter = ('email', 'phone_number')
    fieldsets = (
        (None, {'fields': ('email', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ('user__email', 'phone_number')
    list_filter = ('user__email', 'phone_number')
