from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from django.views import generic


def page_view(request):
    images = LandingPageImage.objects.all()
    phone_categories = PhoneCategoryList.objects.all()
    context = {'images': images, 'categories': phone_categories}
    return render(request, 'front/landing_page.html', context)


def phone_category_view(request, category_id):
    phones = PhoneList.objects.filter(category=category_id)
    return shared_phone_view(request, phones, category_id)


def phone_category_size_view(request, category_id, size):
    phones = PhoneList.objects.filter(category=category_id, size_sku=size)
    size_obj = PhoneMemorySize.objects.get(pk=size)
    size_message = "with a size of " + str(size_obj)
    return shared_phone_view(request, phones, category_id, size_message)


def shared_phone_view(request, phones, category_id, message=""):
    category_pk = PhoneCategoryList.objects.get(pk=category_id)
    phone_categories = PhoneCategoryList.objects.all()
    sizes = PhoneMemorySize.objects.filter(size_category=category_id).order_by('size_number')
    context = {'categories': phone_categories, 'phones': phones,
               'category': category_pk, 'category_id': category_id,
               'size_message': message, 'sizes': sizes, }
    return render(request, 'front/phone_category.html', context)


def sizes(request):
    sizes = PhoneMemorySize.objects.all()
    list_sizes = {}
    size_key = 1
    for size in sizes:
        list_sizes[size_key] = size.size_category
        size_key += 1
    if request.GET["id"] == "":
        filtered_sizes = PhoneMemorySize.objects.filter(size_category=None)
    else:
        filtered_sizes = PhoneMemorySize.objects.filter(
            size_category=request.GET["id"])
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
