from django.shortcuts import render
from .models import LandingPageImage
# Create your views here.
from django.views import generic

def page_view(request):
    images = LandingPageImage.objects.all()
    context = { 'images': images }
    return  render(request, 'front/landing_page.html', context)

def phone_category_view(request):
    return  render(request, 'front/phone_category.html')

def iphone_view(request):
    return  render(request, 'front/iphone.html')

def android_view(request):
    return  render(request, 'front/android.html')

def tablet_view(request):
    return render(request, 'front/tablet.html')

def phone_profile_view(request):
    return render(request, 'front/phone_profile.html')

def phone_view(request):
    return  render(request, 'front/phone.html')
