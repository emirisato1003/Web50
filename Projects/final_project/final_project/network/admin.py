from django.contrib import admin

from .models import User, Categories

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "password")

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("category_name")



admin.site.register(User, UserAdmin)
admin.site.register(Categories)
