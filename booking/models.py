from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import datetime as dt
from multiselectfield import MultiSelectField
from django.dispatch import receiver
from datetime import datetime
from django.utils import timezone

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    profile_photo = models.ImageField(upload_to='profiles/', null=True)
    bio = models.CharField(max_length=240, null=True)
    phone = models.PositiveIntegerField(default=0)
    physical_address = models.CharField(max_length=240, null=True)
    join_date = models.DateTimeField(auto_now_add=True)
    email = models.CharField(max_length=100, blank=True, null=True)

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

        post_save.connect(create_user_profile, sender=User)

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

    @classmethod
    def get_profile(cls):
        profile = Profile.objects.all()
        return profile

    def __str__(self):
        return str(self.user)


class Vehicle(models.Model):
    posted_by = models.ForeignKey(User, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    vehicle_image = models.ImageField(upload_to='picha/', null=True)
    registration = models.CharField(max_length=10, null=True)
    chassis = models.PositiveIntegerField(default=0)
    engine_no = models.PositiveIntegerField(default=0)
    YOM = models.PositiveIntegerField(default=0)

    @classmethod
    def get_vehicles(cls):
        vehicles = Vehicle.objects.all()
        return vehicles

    def __str__(self):
        return str(self.registration)


class Booking(models.Model):
    CHOICES = (
        (1, 'minor service'),
        (2, 'major service'),
        (3, 'bodyshop repairs'),
        (4, 'all'),
    )
    poster = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE,
                                related_name='bookings', null=True)
    service = MultiSelectField(choices=CHOICES, default=0)
    slot_date = models.DateField(default=datetime.now, blank=True)
    slot_time = models.TimeField(default=datetime.now, blank=True)
    slot_end_time = models.TimeField(default=datetime.now, blank=True)
    is_scheduled = models.BooleanField(default=False)

    @classmethod
    def get_booking(cls):
        bookings = Booking.objects.all()
        return bookings

    def __str__(self):
        return str(self.service)
