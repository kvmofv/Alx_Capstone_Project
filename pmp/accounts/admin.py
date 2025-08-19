from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Information", {"fields" : ("phone_number", "role", "gender")}),
    )

    add_fieldsets = (
        (None, {"fields" : ("phone_number", "role", "gender")}),
    )

    list_display = ("email", "username", "role", "is_staff", "is_active")
    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("username", "first_name", "role")
    ordering = ("email", )