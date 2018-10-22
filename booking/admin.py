from django.contrib import admin
from .models import Booking, Profile, Vehicle
# Register your models here.
admin.site.register(Profile)
admin.site.register(Vehicle)
admin.site.register(Booking)
