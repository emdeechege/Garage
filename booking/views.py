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

# Create your views here.


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            current_user = form.save(commit=False)
            current_user.is_active = False
            current_user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your Garage Fix Account.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': current_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(current_user.pk)),
                'token': account_activation_token.make_token(current_user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        current_user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        current_user = None
    if current_user is not None and account_activation_token.check_token(current_user, token):
        current_user.is_active = True
        current_user.save()
        login(request, current_user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. <a href="https://garage-fix.herokuapp.com"> Login </a> Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def welcome(request):
    return render(request, 'index.html')


def home(request):
    if request.user.is_authenticated:
        vehicles = Vehicle.get_vehicles()
        bookings = Booking.get_booking()
        profile = Profile.get_profile()

        current_user = request.user
        if request.method == 'POST':
            form = BookingForm(request.POST)
            if form.is_valid():
                booking = form.save(commit=False)
                booking.user = current_user
                booking.save()
            return redirect('home')

        else:
            form = BookingForm()
            return render(request, "vehicles/home.html", {"vehicles": vehicles, "bookings": bookings, "form": form, "profile": profile})
    else:
        return render(request, "home.html")


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
