from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

# Register your models here.
User = get_user_model()

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'photo' ,'is_staff','is_active')
    list_editable = ('is_staff','is_active')
