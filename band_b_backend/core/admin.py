from django.contrib import admin
from .models import Amenity, House, HouseImage, UserProfile

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ('title', 'admin', 'price', 'address')
    list_filter = ('admin', 'amenities')
    search_fields = ('title', 'address')

@admin.register(HouseImage)
class HouseImageAdmin(admin.ModelAdmin):
    list_display = ('house', 'image')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')