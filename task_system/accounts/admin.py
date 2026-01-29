from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin 
# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username","email","role","is_staff")
        
    fieldsets = UserAdmin.fieldsets + (
        ("Role Infromation",{"fields":("role",)}),
    )
    
    add_fieldsets = ( 
        (None, {
            "classes":("wide",),
            "fields":("username","password1","password2","role"),
        }),
    )