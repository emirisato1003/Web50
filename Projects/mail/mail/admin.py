from django.contrib import admin

# Register your models here.
from .models import User, Email

class AdminUser(admin.ModelAdmin):
    list_display = ("id", "username", "email", "is_staff", "is_active", "date_joined")
    
class AdminEmail(admin.ModelAdmin):
    list_display = ("id", "user", "sender", "subject", "timestamp", "read", "archived", "deleted")
    list_filter = ("read", "archived", "deleted")
    search_fields = ("user", "sender", "subject", "body")
    date_hierarchy = "timestamp"

admin.site.register(User, AdminUser)
admin.site.register(Email, AdminEmail)