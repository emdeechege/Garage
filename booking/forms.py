from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ['poster', 'vehicle']
