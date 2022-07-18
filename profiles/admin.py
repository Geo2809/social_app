from django.contrib import admin
from .models import Profile, Relationship
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    pass

@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    pass