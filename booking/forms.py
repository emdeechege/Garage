from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ['poster', 'vehicle', 'is_scheduled']
        widgets = {
            'slot_date': DatePickerInput(),
            'slot_time': TimePickerInput(),
            'slot_end_time': TimePickerInput(),
        }


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'join_date', 'email']


class UploadForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        exclude = ['posted_by', 'profile']
