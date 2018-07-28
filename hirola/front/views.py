from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from django.views import generic
from django.core.cache import cache


def page_view(request):
    images = cache.get('landing_page_images') or set_cache(
        LandingPageImage.objects.all(),
        'landing_page_images')
    phone_categories = cache.get('phone_categories') or set_cache(
        PhoneCategoryList.objects.all(),
        'phone_categories')
    context = {'images': images, 'categories': phone_categories}
    return render(request, 'front/landing_page.html', context)


def phone_category_view(request, category_id):
    phones = cache.get('phones_{}'.format(category_id)) or set_cache(
        PhoneList.objects.filter(category=category_id),
        'phones_{}'.format(category_id))
    return shared_phone_view(request, phones, category_id)


def phone_category_size_view(request, category_id, size):
    phones = PhoneList.objects.filter(category=category_id, size_sku=size)
    size_obj = PhoneMemorySize.objects.get(pk=size)
    size_message = "with a size of " + str(size_obj)
    return shared_phone_view(request, phones, category_id, size_message)


def shared_phone_view(request, phones, category_id, message=""):
    category_pk = cache.get('category_{}'.format(category_id)) or set_cache(
        PhoneCategoryList.objects.get(pk=category_id),
        'category_{}'.format(category_id))
    phone_categories = cache.get('phone_categories') or set_cache(
        PhoneCategoryList.objects.all(),
        'phone_categories')
    sizes = cache.get('sizes_{}'.format(category_id)) or set_cache(
        PhoneMemorySize.objects.filter(category=category_id).order_by('size_number'),
        'sizes_{}'.format(category_id))
    context = {'categories': phone_categories, 'phones': phones,
               'category': category_pk, 'category_id': category_id,
               'size_message': message, 'sizes': sizes, }
    return render(request, 'front/phone_category.html', context)


def set_cache(data, cache_name):
    cache.set(cache_name, data)
    return data


def sizes(request):
    sizes = PhoneMemorySize.objects.all()
    list_sizes = {}
    size_key = 1
    for size in sizes:
        list_sizes[size_key] = size.category
        size_key += 1
    if request.GET["id"] == "":
        filtered_sizes = PhoneMemorySize.objects.filter(category=None)
    else:
        filtered_sizes = PhoneMemorySize.objects.filter(
            category=request.GET["id"])
    data = {}
    for size in filtered_sizes:
        data[size.pk] = str(size)
    return JsonResponse(data)


def phone_profile_view(request):
    return render(request, 'front/phone_profile.html')


def phone_view(request):
    return render(request, 'front/phone.html')

def about_view(request):
    return render(request, 'front/about.html')

def signup_view(request):
    return render(request, 'front/signup.html')

def login_view(request):
    return render(request, 'front/login.html')
