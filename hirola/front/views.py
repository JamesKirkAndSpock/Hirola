from django.shortcuts import render

# Create your views here.
from django.views import generic

def page_view(request):
    return  render(request, 'front/landing_page.html')

def phone_category_view(request):
    return  render(request, 'front/phone_category.html')

def iphone_view(request):
    return  render(request, 'front/iphone.html')

def android_view(request):
    return  render(request, 'front/android.html')

def phone_view(request):
    return  render(request, 'front/phone.html')
