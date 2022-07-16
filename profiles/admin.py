from django.contrib import admin
from .models import Profile, CustomUser, Relationship


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass
@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    pass