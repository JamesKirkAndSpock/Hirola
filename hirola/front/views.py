from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import *
from django.views import generic
from django.core.cache import cache
from .forms.user_forms import UserCreationForm, AuthenticationForm, UserForm, OldPasswordForm
from django.contrib.auth.views import (PasswordResetView,
 PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from .decorators import old_password_required


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
    (phone_categories,social_media) = various_caches()
    sizes = cache.get('sizes_{}'.format(category_id)) or set_cache(
        PhoneMemorySize.objects.filter(category=category_id).order_by('size_number'),
        'sizes_{}'.format(category_id))
    context = {'categories': phone_categories, 'phones': phones,
               'category': category_pk, 'category_id': category_id,
               'size_message': message, 'sizes': sizes, "social_media": social_media }
    return render(request, 'front/phone_category.html', context)


def set_cache(data, cache_name):
    cache.set(cache_name, data)
    return data


def sizes(request):
    sizes = PhoneMemorySize.objects.all()
    list_sizes = {}
    size_key = 1
    size_id = 0
    for size in sizes:
        list_sizes[size_key] = size.category
        size_key += 1
    if request.GET["id"] == "":
        filtered_sizes = PhoneMemorySize.objects.filter(category=None)
    else:
        filtered_sizes = PhoneMemorySize.objects.filter(
            category=request.GET["id"])
        if PhoneList.objects.filter(pk=request.GET["id"]).first():
            size_id = PhoneList.objects.filter(pk=request.GET["id"]).first().size_sku.pk
    data = {}
    for size in filtered_sizes:
        data[size.pk] = str(size)
    data = {"size_id": size_id, "data": data}
    return JsonResponse(data)

def area_codes(request):
    area_code_data = AreaCode.objects.all()
    users_area_code = request.user.area_code.id
    data = {}
    for area_code in area_code_data:
        data[area_code.pk] = str(area_code)
    data = {"users_area_code": users_area_code, "data": data}
    return JsonResponse(data)

def phone_profile_view(request):
    return render(request, 'front/phone_profile.html')


def phone_view(request):
    return render(request, 'front/phone.html')

def reset_password_view(request):
    return render(request, 'front/reset_password.html')

def new_password_view(request):
    return render(request, 'front/new_password.html')

def checkout_view(request):
    return render(request, 'front/checkout.html')

@login_required
def dashboard_view(request):
    (phone_categories,social_media) = various_caches()
    if request.method == "POST":
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            redirect("/dashboard")
        user = User.objects.get(email=request.user.email)
        context = {"form": form, "user": user, 'categories': phone_categories, "social_media": social_media}
        return render(request, 'front/dashboard.html', context=context)
    context = { "form": UserForm(instance=request.user), "reviews": Reviews.objects.filter(owner=request.user), 'categories': phone_categories, "social_media": social_media}
    return render(request, 'front/dashboard.html', context=context)

def login_view(request):
    (phone_categories,social_media) = various_caches()
    if request.method == "POST":
        form = AuthenticationForm(None, request.POST)
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if form.is_valid() and user is not None:
            login(request, user)
            return redirect('/')
        args = {'form':  form, 'social_media': social_media, 'categories':phone_categories}
        return render(request, 'front/login.html', args)
    args = {'form':  AuthenticationForm(), 'social_media': social_media, 'categories':phone_categories}
    return render(request, 'front/login.html', args)

def logout_view(request):
    logout(request)


def about_view(request):
    (phone_categories,social_media) = various_caches()
    context = {"categories": phone_categories, "social_media": social_media}
    return render(request, 'front/about.html', context=context)


def signup_view(request):
    (phone_categories,social_media) = various_caches()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        args = {'form':  form, 'social_media': social_media, 'categories':phone_categories}
        return render(request, 'front/signup.html', args)
    else:
        args = {'form':  UserCreationForm(), 'social_media': social_media, 'categories':phone_categories}
        return render(request, 'front/signup.html', args)


def imei_view(request):
    return render(request, 'front/imei.html')


class PasswordResetViewTailored(PasswordResetView):

    success_url = reverse_lazy('password_reset_done', urlconf='front.urls')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = cache.get('phone_categories') or set_cache(
            PhoneCategoryList.objects.all(),
            'phone_categories')
        context['social_media'] = cache.get('social_media') or set_cache(
            SocialMedia.objects.all(), 'social_media')
        return context

class PasswordResetConfirmViewTailored(PasswordResetConfirmView):

    success_url = reverse_lazy('password_reset_complete', urlconf='front.urls')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.user
        (context['categories'], context['social_media']) = various_caches()
        return context


@login_required
@old_password_required
def change_password_view(request):
    (phone_categories,social_media) = various_caches()
    if request.method == 'POST':
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.get(email=request.user.email)
            user.is_change_allowed = False
            user.save()
            return redirect('/login')
        args = {"form": form, 'social_media': social_media, 'categories':phone_categories}
        return render(request, 'front/change_password.html', args)
    args = {"form": SetPasswordForm(request.user), 'social_media': social_media, 'categories':phone_categories}
    return render(request, 'front/change_password.html', args)


@login_required
def old_password_view(request):
    (phone_categories,social_media) = various_caches()
    if request.method == 'POST':
        form = OldPasswordForm(request.user, request.POST)
        if form.is_valid():
            user = User.objects.get(email=request.user.email)
            user.is_change_allowed = True
            user.save()
            return redirect('/change_password')
        args = {'form':  form, 'social_media': social_media, 'categories':phone_categories}
        return render(request, 'front/old_password.html', args)
    args = {"form": OldPasswordForm(request.user), 'social_media': social_media, 'categories':phone_categories}
    return render(request, 'front/old_password.html', args)


def various_caches():
    phone_categories = cache.get('phone_categories') or set_cache(
        PhoneCategoryList.objects.all(),
        'phone_categories')
    social_media = cache.get('social_media') or set_cache(
        SocialMedia.objects.all(), 'social_media')
    return (phone_categories, social_media)