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

def phone_view(request):
    return  render(request, 'front/phone.html')
