from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    profile_photo = models.ImageField(upload_to='profiles/', null=True)
    bio = models.CharField(max_length=240, null=True)
    phone = models.PositiveIntegerField(default=0)
    physical_address = models.CharField(max_length=240, null=True)

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

    class Meta:
        ordering = ['user']
