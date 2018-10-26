from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib import messages

import datetime
from datetime import timedelta
import pytz
from googleapiclient.discovery import build
from oauth2client import file, client, tools
# Create your views here.


def welcome(request):
    return render(request, 'index.html')


def home(request):
    if request.user.is_authenticated:
        vehicles = Vehicle.objects.filter(posted_by=request.user).all()
        bookings = Booking.objects.filter(poster=request.user).all()
        profile = Profile.objects.get(user=request.user)

        current_user = request.user
        if request.method == 'POST':
            form = BookingForm(request.POST)
            if form.is_valid():
                booking = form.save(commit=False)
                booking.poster = current_user
                booking.save()
            return redirect('home')

        else:
            form = BookingForm()
            return render(request, "vehicles/home.html", {"vehicles": vehicles, "bookings": bookings, "form": form, "profile": profile})
    else:
        return render(request, "vehicles/home.html")


@login_required(login_url='/accounts/login/')
def profile(request):
    profile = Profile.objects.get(user=request.user)
    vehicle = Vehicle.objects.filter(posted_by=request.user).all()

    return render(request, 'profiles/profile.html', {"profile": profile, "vehicle": vehicle})


@login_required(login_url='/accounts/login/')
def edit_profile(request):
    current_user = request.user
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = current_user
            profile.email = current_user.email
            profile.save()
        return redirect('profile')

    else:
        form = EditProfileForm(instance=profile)
    return render(request, 'profiles/edit_profile.html', {"form": form})


@login_required(login_url='/accounts/login/')
def update_vehicle(request):
    current_user = request.user
    profiles = Profile.get_profile()
    for profile in profiles:
        if profile.user.id == current_user.id:
            if request.method == 'POST':
                form = UploadForm(request.POST, request.FILES)
                if form.is_valid():
                    upload = form.save(commit=False)
                    upload.posted_by = current_user
                    upload.profile = profile
                    upload.save()
                    return redirect('home')
            else:
                form = UploadForm()
            return render(request, 'vehicles/upload.html', {"user": current_user, "form": form})


@login_required(login_url='/accounts/login/')
def add_booking(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    current_user = request.user
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.vehicle = vehicle
            booking.poster = current_user
            booking.save()
            return redirect('home')
    else:
        form = BookingForm()
        return render(request, 'vehicles/booking.html', {"user": current_user, "booking_form": form})
